from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paciente

@login_required
def detalle(request, pk):
    paciente = get_object_or_404(Paciente.objects.prefetch_related(
        'consentimientos__plantilla', 'consentimientos__odontologo'), pk=pk)
    return render(request, 'pacientes/detalle.html', {'paciente': paciente})

@login_required
def lista(request):
    q = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.filter(activo=True)
    if q:
        from django.db.models import Q
        pacientes = pacientes.filter(
            Q(nombres__icontains=q)|Q(apellidos__icontains=q)|Q(documento__icontains=q))
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes, 'q': q})
