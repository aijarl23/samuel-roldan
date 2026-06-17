from .base import *
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
