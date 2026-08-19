"""
Definición única de qué puede hacer cada rol (grupo de Django). La usan tanto
setup_inicial.py (aprovisionamiento en cada deploy) como la batería de pruebas
automatizadas, para que nunca queden desincronizados entre sí.
"""
from django.contrib.auth.models import Group, Permission

PERMISOS_ODONTOLOGO = [
    'view_paciente', 'add_paciente', 'change_paciente',
    'view_consentimiento', 'add_consentimiento', 'change_consentimiento',
    'view_plantillaconsentimiento',
    # Historia clínica: registrar evoluciones/odontograma es responsabilidad
    # exclusiva del odontólogo, no del auxiliar.
    'view_fichaclinica', 'add_fichaclinica', 'change_fichaclinica',
    'view_evolucionclinica', 'add_evolucionclinica', 'change_evolucionclinica',
    'view_odontograma', 'add_odontograma', 'change_odontograma',
]

PERMISOS_AUXILIAR = [
    'view_paciente', 'add_paciente', 'change_paciente',
    'view_consentimiento', 'add_consentimiento',
    'view_plantillaconsentimiento',
    # Solo consulta de historia clínica, no puede registrar evoluciones.
    'view_fichaclinica', 'view_evolucionclinica', 'view_odontograma',
]

APPS_CLINICAS = ['pacientes', 'consentimientos', 'historial']


def configurar_grupos():
    """Crea (si no existen) los grupos Odontologo/Auxiliar y les asigna sus
    permisos. Idempotente: se puede llamar en cada deploy y en cada test."""
    perms = Permission.objects.filter(content_type__app_label__in=APPS_CLINICAS)

    rol_od, _ = Group.objects.get_or_create(name='Odontologo')
    rol_od.permissions.set(perms.filter(codename__in=PERMISOS_ODONTOLOGO))

    rol_aux, _ = Group.objects.get_or_create(name='Auxiliar')
    rol_aux.permissions.set(perms.filter(codename__in=PERMISOS_AUXILIAR))

    return rol_od, rol_aux
