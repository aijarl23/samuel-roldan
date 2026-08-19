from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.core.exceptions import ValidationError

MAX_INTENTOS = 5
BLOQUEO_SEGUNDOS = 15 * 60


def _cache_key(request, username):
    ip = request.META.get('REMOTE_ADDR', 'sin-ip')
    return f'login_intentos:{ip}:{username.lower().strip()}'


class ThrottledAuthenticationForm(AuthenticationForm):
    """Bloquea intentos de login tras varios fallos consecutivos para el
    mismo usuario+IP. Mitigación básica de fuerza bruta (cache por proceso,
    no sustituye un límite centralizado en Redis para despliegues con
    múltiples workers)."""

    def clean(self):
        username = self.cleaned_data.get('username') or self.data.get('username', '')
        if username:
            key = _cache_key(self.request, username)
            if cache.get(key, 0) >= MAX_INTENTOS:
                raise ValidationError(
                    'Demasiados intentos fallidos. Espera unos minutos antes de volver a intentar.',
                    code='throttled',
                )
        return super().clean()
