import os
from pathlib import Path
import dj_database_url
import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Directorio de datos persistentes: si Railway tiene un Volume montado en
# /data, la base de datos SQLite y los archivos subidos (fotos, PDFs
# firmados) viven ahí y sobreviven a cada deploy. Sin volumen (dev local),
# caen de vuelta a la carpeta del proyecto.
_VOLUMEN = Path('/data')
DATA_DIR = _VOLUMEN if _VOLUMEN.is_dir() else BASE_DIR

# En Railway las variables ya están en el entorno del proceso: read_env() no
# hace nada si no encuentra .env. En local, carga las variables de .env
# (copiado de .env.example) sin necesidad de exportarlas manualmente.
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

if DEBUG:
    # Solo para desarrollo local. En producción (DEBUG=False) la SECRET_KEY
    # es obligatoria por variable de entorno: si falta, la app no arranca
    # en vez de firmar sesiones/CSRF con una clave adivinable.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-local-samuel-2026-solo-dev')
else:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ImproperlyConfigured(
            'La variable de entorno SECRET_KEY es obligatoria en producción. '
            'Configúrala en las variables de entorno de Railway.')

ALLOWED_HOSTS = [h.strip() for h in os.environ.get(
    'ALLOWED_HOSTS',
    'samuel-roldan-production.up.railway.app,localhost,127.0.0.1'
).split(',') if h.strip()]

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'https://samuel-roldan-production.up.railway.app,https://*.up.railway.app,'
    'http://localhost:8005,http://127.0.0.1:8005'
).split(',') if o.strip()]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    # Endurecimiento de sesión/cookies — solo aplica sobre HTTPS (Railway
    # termina TLS y reenvía por SECURE_PROXY_SSL_HEADER arriba).
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# Cierre de sesión por inactividad (jornada clínica): 8 horas, renovable
# en cada request mientras el usuario esté activo.
SESSION_COOKIE_AGE = 8 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

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
        'NAME': DATA_DIR / 'db.sqlite3',
    }}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'consentimientos': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

GOOGLE_DRIVE_CREDENTIALS = os.environ.get('GOOGLE_DRIVE_CREDENTIALS', '')
GOOGLE_DRIVE_FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', '')

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'Clínica R — Samuel Roldán <noreply@clinica-r.co>')
# Sin credenciales SMTP configuradas, los correos se escriben en el log en
# vez de fallar o quedar "enviados" en silencio sin llegar a nadie.
EMAIL_BACKEND = ('django.core.mail.backends.smtp.EmailBackend' if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
                  else 'django.core.mail.backends.console.EmailBackend')
