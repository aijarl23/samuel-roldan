from django.contrib.auth.views import LoginView
from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.core.cache import cache
from django.dispatch import receiver

from .forms import ThrottledAuthenticationForm, _cache_key, BLOQUEO_SEGUNDOS


class ThrottledLoginView(LoginView):
    form_class = ThrottledAuthenticationForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get('form')
        ctx['throttled'] = bool(form and form.has_error('__all__', code='throttled'))
        return ctx


@receiver(user_login_failed)
def _registrar_intento_fallido(sender, credentials=None, request=None, **kwargs):
    if not request:
        return
    username = (credentials or {}).get('username', '')
    if not username:
        return
    key = _cache_key(request, username)
    cache.set(key, cache.get(key, 0) + 1, BLOQUEO_SEGUNDOS)


@receiver(user_logged_in)
def _limpiar_intentos(sender, request=None, user=None, **kwargs):
    if request and user:
        cache.delete(_cache_key(request, user.username))
