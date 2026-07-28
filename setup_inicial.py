import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_prod")
import django
django.setup()

from django.contrib.auth.models import User, Group, Permission
from consentimientos.models import PlantillaConsentimiento

# Solo crea admin si NO existe
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@clinica-r.co", "ClinicaR2026#Admin")
    print("Superusuario admin creado.")
else:
    print("Admin ya existe - clave NO modificada.")

# Roles
apps = ["pacientes", "consentimientos", "historial"]
perms = Permission.objects.filter(content_type__app_label__in=apps)
rol_od, _ = Group.objects.get_or_create(name="Odontologo")
rol_od.permissions.set(perms.filter(codename__in=[
    "view_paciente","add_paciente","change_paciente",
    "view_consentimiento","add_consentimiento","change_consentimiento",
    "view_plantillaconsentimiento",
]))
rol_aux, _ = Group.objects.get_or_create(name="Auxiliar")
rol_aux.permissions.set(perms.filter(codename__in=[
    "view_paciente","add_paciente","change_paciente",
    "view_consentimiento","add_consentimiento",
    "view_plantillaconsentimiento",
]))
print("Roles configurados.")

# Plantillas
admin_user = User.objects.filter(username="admin").first()
plantillas = [
    ("Consentimiento Informado - Ortodoncia", "ORTODONCIA"),
    ("Consentimiento Informado - Endodoncia", "ENDODONCIA"),
    ("Consentimiento Informado - Exodoncia",  "EXODONCIA"),
]
for nombre, tipo in plantillas:
    obj, created = PlantillaConsentimiento.objects.get_or_create(
        nombre=nombre,
        defaults={"tipo": tipo, "texto": nombre, "version": 1,
                  "activa": True, "creado_por": admin_user,
                  "requiere_autorizacion_expediente": True}
    )
    if created:
        print(f"Plantilla creada: {nombre}")

print("Sistema listo.")
