"""
Ejecutar en C:\\samuel_roldan:
  python fix_railway.py
  git add -A
  git commit -m "fix railway"
  git push
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# 1. wsgi.py apuntando a settings unico
with open(os.path.join(BASE, 'config', 'wsgi.py'), 'w', encoding='utf-8') as f:
    f.write("""import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_prod')
application = get_wsgi_application()
""")
print("OK wsgi.py")

# 2. settings_prod.py — archivo unico sin subcarpeta
with open(os.path.join(BASE, 'config', 'settings_prod.py'), 'w', encoding='utf-8') as f:
    f.write("""import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-local-samuel-2026')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-92666.up.railway.app',
    'https://*.up.railway.app',
    'http://localhost:8005',
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auditlog',
    'accounts',
    'pacientes',
    'consentimientos',
    'historial',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.LoginRequiredMiddleware',
    'config.middleware.RoleContextMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'config.context_processors.globals',
    ]},
}]

DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

GOOGLE_DRIVE_CREDENTIALS = os.environ.get('GOOGLE_DRIVE_CREDENTIALS', '')
GOOGLE_DRIVE_FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', '')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Consultorio Samuel Roldan <noreply@samuelroldan.co>'
""")
print("OK config/settings_prod.py")

# 3. Procfile
with open(os.path.join(BASE, 'Procfile'), 'w', encoding='utf-8') as f:
    f.write("web: python manage.py migrate --settings=config.settings_prod && python setup_inicial.py && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2\n")
print("OK Procfile")

# 4. manage.py apuntando a settings_prod
with open(os.path.join(BASE, 'manage.py'), 'w', encoding='utf-8') as f:
    f.write("""#!/usr/bin/env python
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
print("OK manage.py")

print("\n=== LISTO ===")
print("Ahora ejecuta:")
print("  git add -A")
print("  git commit -m 'fix railway settings'")
print("  git push")
