from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from .models import Paciente
from .forms import PacienteRapidoForm

@login_required
@permission_required('pacientes.view_paciente', raise_exception=True)
def detalle(request, pk):
    """Ficha del Paciente — pantalla central del sistema. Reúne datos del
    paciente, consentimientos y un resumen de historia clínica en una sola
    vista, para minimizar navegación (no reemplaza /historial/paciente/<pk>/,
    que sigue disponible para el detalle completo de evoluciones)."""
    paciente = get_object_or_404(Paciente.objects.prefetch_related(
        'consentimientos__plantilla', 'consentimientos__odontologo'), pk=pk)
    ficha_clinica = None
    ultimas_evoluciones = []
    try:
        from historial.models import FichaClinica
        ficha_clinica = FichaClinica.objects.filter(paciente=paciente).select_related('odontologo_principal').first()
        if ficha_clinica:
            ultimas_evoluciones = ficha_clinica.evoluciones.select_related('odontologo').order_by('-fecha')[:5]
    except Exception:
        pass
    from consentimientos.models import PlantillaConsentimiento
    tipos_disponibles = PlantillaConsentimiento.objects.filter(activa=True).order_by('nombre')
    return render(request, 'pacientes/detalle.html', {
        'paciente': paciente,
        'ficha_clinica': ficha_clinica,
        'ultimas_evoluciones': ultimas_evoluciones,
        'tipos_disponibles': tipos_disponibles,
    })

@login_required
@permission_required('pacientes.view_paciente', raise_exception=True)
def lista(request):
    q = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.filter(activo=True)
    if q:
        pacientes = pacientes.filter(
            Q(nombres__icontains=q)|Q(apellidos__icontains=q)|Q(documento__icontains=q))
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes, 'q': q})


@login_required
@permission_required('pacientes.view_paciente', raise_exception=True)
def buscar_json(request):
    """Endpoint del buscador global en vivo (barra superior). Nunca navega:
    alimenta el dropdown de resultados con fetch()."""
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'pacientes': []})
    pacientes = (Paciente.objects.filter(activo=True)
                 .filter(Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(documento__icontains=q))
                 .order_by('apellidos', 'nombres')[:8])
    data = [{
        'nombre': p.nombre_completo,
        'documento': p.documento,
        'tipo_doc': p.get_tipo_documento_display(),
        'url': reverse('pacientes:detalle', args=[p.pk]),
        'pendientes': p.consentimientos.filter(estado='PENDIENTE').count(),
    } for p in pacientes]
    return JsonResponse({'pacientes': data})


@login_required
@permission_required('pacientes.add_paciente', raise_exception=True)
def crear_panel(request):
    """Fragmento HTML servido dentro del drawer lateral (no es una página completa).
    GET: muestra el formulario. POST (AJAX): valida y crea, responde JSON con
    la URL de la Ficha del Paciente recién creado, o vuelve a renderizar el
    formulario con errores si algo falta."""
    q_inicial = request.GET.get('q', '')
    if request.method == 'POST':
        form = PacienteRapidoForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return JsonResponse({'redirect': reverse('pacientes:detalle', args=[paciente.pk])})
        html = render(request, 'pacientes/_crear_panel.html', {'form': form}).content.decode('utf-8')
        return JsonResponse({'html': html}, status=400)

    nombres_iniciales = {}
    if q_inicial and not q_inicial.replace(' ', '').isdigit():
        nombres_iniciales['nombres'] = q_inicial
    elif q_inicial:
        nombres_iniciales['documento'] = q_inicial
    form = PacienteRapidoForm(initial=nombres_iniciales)
    return render(request, 'pacientes/_crear_panel.html', {'form': form})
