"""
Ejecutar en C:\\samuel_roldan:
  python crear_settings.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(BASE, 'config', 'settings_prod.py')

contenido = (
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
    "DEFAULT_FROM_EMAIL = 'Consultorio Samuel Roldan <noreply@samuelroldan.co>'\n"
)

with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
    f.write(contenido)

# Verificar
with open(ruta, 'rb') as f:
    data = f.read()
nulls = data.count(b'\x00')
print(f"OK - archivo creado: {len(data)} bytes, bytes nulos: {nulls}")
print(f"Ruta: {ruta}")
print("\nAhora ejecuta:")
print("  git add config/settings_prod.py")
print("  git commit -m 'settings sin null bytes'")
print("  git push")
