import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import FileResponse, JsonResponse, Http404
from django.urls import reverse
from django.utils import timezone
from django.core.files import File
from django.db.models import Count, Q
from django.views.decorators.http import require_POST

from pacientes.models import Paciente
from .models import Consentimiento, PlantillaConsentimiento
from .services import pdf as pdf_svc
from .services import drive as drive_svc
from .services import notificaciones as notif_svc

logger = logging.getLogger(__name__)


@login_required
@permission_required('consentimientos.add_consentimiento', raise_exception=True)
def asistente(request, paciente_pk):
    """Paso 1 del asistente de consentimiento (drawer): elegir el tipo de
    plantilla. Al confirmar, crea el Consentimiento en estado PENDIENTE y
    entrega la URL de la vista `firmar` ya existente — la captura de firma,
    generación de PDF y notificaciones NO se duplican, se reutilizan tal cual."""
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    tipos = PlantillaConsentimiento.objects.filter(activa=True).order_by('nombre')

    if request.method == 'POST':
        plantilla_id = request.POST.get('plantilla_id')
        plantilla = get_object_or_404(PlantillaConsentimiento, pk=plantilla_id, activa=True)
        c = Consentimiento.objects.create(
            paciente=paciente, plantilla=plantilla,
            odontologo=request.user, creado_por=request.user,
            estado='PENDIENTE',
        )
        if not request.user.has_perm('consentimientos.change_consentimiento'):
            # Auxiliar: puede crearlo pero no firmarlo; queda pendiente para el odontólogo.
            messages.success(request, 'Consentimiento creado y pendiente de firma por el odontólogo.')
            return JsonResponse({'redirect': reverse('pacientes:detalle', args=[paciente.pk])})
        return JsonResponse({'redirect': reverse('consentimientos:firmar', args=[c.pk])})

    return render(request, 'consentimientos/_asistente_panel.html', {
        'paciente': paciente, 'tipos': tipos,
    })


@login_required
@permission_required('consentimientos.view_consentimiento', raise_exception=True)
def panel(request):
    hoy = timezone.localdate()
    ctx = {
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'pendientes': Consentimiento.objects.filter(estado='PENDIENTE').count(),
        'firmados_hoy': Consentimiento.objects.filter(
            estado='FIRMADO', fecha_firma__date=hoy).count(),
        'firmados_mes': Consentimiento.objects.filter(
            estado='FIRMADO',
            fecha_firma__year=hoy.year,
            fecha_firma__month=hoy.month).count(),
        'recientes': Consentimiento.objects.select_related(
            'paciente', 'plantilla', 'odontologo').order_by('-creado')[:15],
        'pendientes_lista': Consentimiento.objects.filter(
            estado='PENDIENTE').select_related('paciente', 'plantilla')[:10],
    }
    return render(request, 'base/panel.html', ctx)


@login_required
@permission_required('consentimientos.change_consentimiento', raise_exception=True)
def firmar(request, pk):
    """Vista de firma — optimizada para touch en tablet/celular."""
    c = get_object_or_404(
        Consentimiento.objects.select_related('paciente', 'plantilla', 'odontologo'), pk=pk)

    if c.estado == 'FIRMADO':
        messages.info(request, 'Este consentimiento ya fue firmado.')
        return redirect('panel')
    if c.estado == 'ANULADO':
        messages.error(request, 'Este consentimiento está anulado.')
        return redirect('panel')

    if request.method == 'POST':
        firma_p = request.POST.get('firma_paciente', '').strip()
        firma_a = request.POST.get('firma_acudiente', '').strip()
        _pref = 'data:image/png;base64,'
        _max = 4 * 1024 * 1024
        for _f in (firma_p, firma_a):
            if _f and (not _f.startswith(_pref) or len(_f) > _max):
                messages.error(request, 'Imagen de firma no válida.')
                return redirect('consentimientos:firmar', pk=pk)
        if not firma_p or len(firma_p) < 50:
            messages.error(request, 'Debe registrar la firma del paciente.')
            return redirect('consentimientos:firmar', pk=pk)

        if c.paciente.es_menor and not request.POST.get('firma_acudiente', '').strip():
            messages.error(request, 'El paciente es menor de edad. Se requiere firma del acudiente.')
            return redirect('consentimientos:firmar', pk=pk)

        # Guardar firma y generar documentación
        c.firma_paciente = firma_p
        c.firma_acudiente = request.POST.get('firma_acudiente', '')
        auth = request.POST.get('autoriza_expediente')
        c.autoriza_expediente = True if auth == 'si' else (False if auth == 'no' else None)
        c.texto_generado = c.generar_texto()
        c.fecha_firma = timezone.now()
        c.ip_firma = _get_ip(request)
        c.dispositivo = request.META.get('HTTP_USER_AGENT', '')[:512]
        c.estado = 'FIRMADO'
        c.hash_documento = c.calcular_hash()
        c.save()

        # Generar PDF
        try:
            ruta = pdf_svc.generar(c)
            with open(ruta, 'rb') as fh:
                c.pdf.save(f'consent_{c.id:06d}.pdf', File(fh), save=False)
            c.drive_url = drive_svc.subir_pdf(c, ruta)
            c.save(update_fields=['pdf', 'drive_url'])
        except Exception as e:
            logger.error('Error generando PDF consentimiento %d: %s', c.id, e)
            messages.warning(request, 'Consentimiento firmado, pero hubo un error al generar el PDF. Notifique al administrador.')
            return redirect('panel')

        # Notificaciones (no bloquean si fallan)
        notif_svc.enviar_correo(c)
        notif_svc.enviar_whatsapp(c)

        messages.success(request,
            f'✅ Consentimiento firmado correctamente para {c.paciente.nombre_completo}.')
        return redirect('consentimientos:detalle', pk=c.pk)

    texto_preview = c.generar_texto()
    return render(request, 'consentimientos/firmar.html', {'c': c, 'texto': texto_preview})


@login_required
@permission_required('consentimientos.view_consentimiento', raise_exception=True)
def detalle(request, pk):
    c = get_object_or_404(
        Consentimiento.objects.select_related('paciente', 'plantilla', 'odontologo', 'creado_por'), pk=pk)
    return render(request, 'consentimientos/detalle.html', {'c': c})


@login_required
@permission_required('consentimientos.view_consentimiento', raise_exception=True)
def ver_pdf(request, pk):
    c = get_object_or_404(Consentimiento, pk=pk)
    if not c.pdf:
        raise Http404('PDF no disponible')
    return FileResponse(c.pdf.open('rb'), content_type='application/pdf',
                        filename=f'consentimiento_{c.paciente.documento}.pdf')


@login_required
@permission_required('consentimientos.view_consentimiento', raise_exception=True)
def lista_paciente(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    consentimientos = paciente.consentimientos.select_related(
        'plantilla', 'odontologo').order_by('-creado')
    return render(request, 'consentimientos/lista_paciente.html',
                  {'paciente': paciente, 'consentimientos': consentimientos})


def _get_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')
