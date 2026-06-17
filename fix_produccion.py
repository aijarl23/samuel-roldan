import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Reescribir production.py completo y correcto
prod = os.path.join(BASE, 'config', 'settings', 'production.py')
with open(prod, 'w', encoding='utf-8') as f:
    f.write("""from .base import *
import dj_database_url, os, environ

env = environ.Env()

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-92666.up.railway.app',
    'https://*.up.railway.app',
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1, 'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'WARNING'},
}
""")
print("OK production.py corregido")

# Reescribir wsgi.py
wsgi = os.path.join(BASE, 'config', 'wsgi.py')
with open(wsgi, 'w', encoding='utf-8') as f:
    f.write("""import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()
""")
print("OK wsgi.py corregido")

# Reescribir Procfile
proc = os.path.join(BASE, 'Procfile')
with open(proc, 'w', encoding='utf-8') as f:
    f.write("web: python manage.py migrate && python setup_inicial.py && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2\n")
print("OK Procfile corregido")

print("\nListo. Ahora ejecuta:")
print("  git add -A")
print("  git commit -m 'fix produccion'")
print("  git push")
