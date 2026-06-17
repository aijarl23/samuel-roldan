from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FichaClinica
from pacientes.models import Paciente

@login_required
def ficha(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    ficha, _ = FichaClinica.objects.select_related('odontologo_principal').get_or_create(
        paciente=paciente,
        defaults={'creado_por': request.user, 'odontologo_principal': request.user})
    evoluciones = ficha.evoluciones.select_related('odontologo').order_by('-fecha')
    return render(request, 'historial/ficha.html', {'paciente': paciente, 'ficha': ficha, 'evoluciones': evoluciones})
