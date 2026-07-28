"""
FIX DEFINITIVO — Local y Railway
Ejecutar en C:\\samuel_roldan con venv activo:
  python fix_total.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def w(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
        f.write(contenido)
    print(f'  OK -> {os.path.relpath(ruta, BASE)}')

print("\n=== FIX DEFINITIVO SAMUEL ROLDÁN ===\n")

# ── 1. Procfile correcto ──────────────────────────────────────────────────
w(os.path.join(BASE, 'Procfile'),
  "web: python manage.py collectstatic --noinput && python manage.py migrate && python setup_inicial.py && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2\n")

# ── 2. manage.py apuntando a settings_prod ────────────────────────────────
w(os.path.join(BASE, 'manage.py'), """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_prod')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError('No se pudo importar Django.') from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""")

# ── 3. wsgi.py ────────────────────────────────────────────────────────────
w(os.path.join(BASE, 'config', 'wsgi.py'), """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_prod')
application = get_wsgi_application()
""")

# ── 4. settings_prod.py limpio ────────────────────────────────────────────
w(os.path.join(BASE, 'config', 'settings_prod.py'),
"import os\n"
"from pathlib import Path\n"
"import dj_database_url\n"
"\n"
"BASE_DIR = Path(__file__).resolve().parent.parent\n"
"\n"
"SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-local-samuel-2026')\n"
"DEBUG = os.environ.get('DEBUG', 'False') == 'True'\n"
"ALLOWED_HOSTS = ['*']\n"
"CSRF_TRUSTED_ORIGINS = [\n"
"    'https://samuel-roldan-production.up.railway.app',\n"
"    'https://*.up.railway.app',\n"
"    'http://localhost:8005',\n"
"    'http://127.0.0.1:8005',\n"
"]\n"
"SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')\n"
"\n"
"INSTALLED_APPS = [\n"
"    'django.contrib.admin',\n"
"    'django.contrib.auth',\n"
"    'django.contrib.contenttypes',\n"
"    'django.contrib.sessions',\n"
"    'django.contrib.messages',\n"
"    'django.contrib.staticfiles',\n"
"    'auditlog',\n"
"    'accounts',\n"
"    'pacientes',\n"
"    'consentimientos',\n"
"    'historial',\n"
"]\n"
"\n"
"MIDDLEWARE = [\n"
"    'django.middleware.security.SecurityMiddleware',\n"
"    'whitenoise.middleware.WhiteNoiseMiddleware',\n"
"    'django.contrib.sessions.middleware.SessionMiddleware',\n"
"    'django.middleware.common.CommonMiddleware',\n"
"    'django.middleware.csrf.CsrfViewMiddleware',\n"
"    'django.contrib.auth.middleware.AuthenticationMiddleware',\n"
"    'auditlog.middleware.AuditlogMiddleware',\n"
"    'django.contrib.messages.middleware.MessageMiddleware',\n"
"    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n"
"    'config.middleware.LoginRequiredMiddleware',\n"
"    'config.middleware.RoleContextMiddleware',\n"
"]\n"
"\n"
"ROOT_URLCONF = 'config.urls'\n"
"WSGI_APPLICATION = 'config.wsgi.application'\n"
"\n"
"TEMPLATES = [{\n"
"    'BACKEND': 'django.template.backends.django.DjangoTemplates',\n"
"    'DIRS': [BASE_DIR / 'templates'],\n"
"    'APP_DIRS': True,\n"
"    'OPTIONS': {'context_processors': [\n"
"        'django.template.context_processors.debug',\n"
"        'django.template.context_processors.request',\n"
"        'django.contrib.auth.context_processors.auth',\n"
"        'django.contrib.messages.context_processors.messages',\n"
"        'config.context_processors.globals',\n"
"    ]},\n"
"}]\n"
"\n"
"DATABASE_URL = os.environ.get('DATABASE_URL', '')\n"
"if DATABASE_URL:\n"
"    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}\n"
"else:\n"
"    DATABASES = {'default': {\n"
"        'ENGINE': 'django.db.backends.sqlite3',\n"
"        'NAME': BASE_DIR / 'db.sqlite3',\n"
"    }}\n"
"\n"
"LANGUAGE_CODE = 'es-co'\n"
"TIME_ZONE = 'America/Bogota'\n"
"USE_I18N = True\n"
"USE_TZ = True\n"
"\n"
"STATIC_URL = '/static/'\n"
"STATICFILES_DIRS = [BASE_DIR / 'static']\n"
"STATIC_ROOT = BASE_DIR / 'staticfiles'\n"
"STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'\n"
"MEDIA_URL = '/media/'\n"
"MEDIA_ROOT = BASE_DIR / 'media'\n"
"\n"
"DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'\n"
"LOGIN_URL = '/accounts/login/'\n"
"LOGIN_REDIRECT_URL = '/'\n"
"LOGOUT_REDIRECT_URL = '/accounts/login/'\n"
"\n"
"GOOGLE_DRIVE_CREDENTIALS = os.environ.get('GOOGLE_DRIVE_CREDENTIALS', '')\n"
"GOOGLE_DRIVE_FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '')\n"
"TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')\n"
"TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')\n"
"TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', '')\n"
"EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'\n"
"DEFAULT_FROM_EMAIL = 'Clinica R Samuel Roldan <noreply@clinica-r.co>'\n"
)

# ── 5. setup_inicial.py que NO resetea clave ──────────────────────────────
w(os.path.join(BASE, 'setup_inicial.py'), """import os, sys
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
""")

print("\n=== LISTO ===")
print("\nPrueba local:")
print("  python manage.py runserver 0.0.0.0:8005")
print("\nPara Railway:")
print("  git add -A")
print("  git commit -m 'fix total settings y procfile'")
print("  git push")
