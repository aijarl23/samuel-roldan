import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_prod")
import django
django.setup()

from django.contrib.auth.models import User
from accounts.roles import configurar_grupos
from consentimientos.models import PlantillaConsentimiento

# La clave del admin NUNCA se hardcodea en el repositorio: solo existe,
# temporalmente, en la variable de entorno DJANGO_ADMIN_PASSWORD (Railway →
# Variables). Este bloque cubre los dos casos:
#   - "admin" no existe todavía  -> lo crea con esa clave.
#   - "admin" ya existe (caso típico si perdiste el acceso) -> RESTABLECE
#     su contraseña a esa misma variable, sin tocar nada más de la cuenta.
# En ambos casos: define DJANGO_ADMIN_PASSWORD, despliega, entra, y borra la
# variable de Railway — no debe quedar guardada una vez usada.
admin_password = os.environ.get("DJANGO_ADMIN_PASSWORD")
admin_user = User.objects.filter(username="admin").first()

if admin_user is None:
    if admin_password:
        admin_user = User.objects.create_superuser("admin", "admin@clinica-r.co", admin_password)
        print("Superusuario admin creado con la clave de DJANGO_ADMIN_PASSWORD.")
    else:
        print("DJANGO_ADMIN_PASSWORD no está definida: no se creó ningún superusuario. "
              "Define esa variable en Railway y vuelve a desplegar, o ejecuta "
              "'python manage.py createsuperuser' manualmente.")
elif admin_password:
    admin_user.set_password(admin_password)
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.is_active = True
    admin_user.save()
    print("Contraseña de admin RESTABLECIDA desde DJANGO_ADMIN_PASSWORD. "
          "Borra esa variable de Railway ahora que ya la usaste.")
else:
    print("Admin ya existe - clave NO modificada (DJANGO_ADMIN_PASSWORD no está definida).")

# Roles (definición única en accounts/roles.py, compartida con las pruebas)
configurar_grupos()
print("Roles configurados.")

# Plantillas
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
