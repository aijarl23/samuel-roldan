from .base import *
import dj_database_url, os

DEBUG = False
SECRET_KEY = env('SECRET_KEY')

if env('DATABASE_URL', default=''):
    DATABASES = {'default': dj_database_url.parse(env('DATABASE_URL'), conn_max_age=600)}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1, 'disable_existing_loggers': False,
    'handlers': {'file': {'class': 'logging.FileHandler', 'filename': BASE_DIR / 'logs/django.log'}},
    'root': {'handlers': ['file'], 'level': 'WARNING'},
}
