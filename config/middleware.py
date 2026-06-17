from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    EXEMPT = ['/accounts/login/', '/admin/login/', '/static/', '/media/', '/favicon.ico']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(request.path.startswith(p) for p in self.EXEMPT):
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return self.get_response(request)


class RoleContextMiddleware:
    """Adjunta el rol activo al request para usar en templates y vistas."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            grupos = list(request.user.groups.values_list('name', flat=True))
            request.es_admin = request.user.is_superuser or 'Administrador' in grupos
            request.es_odontologo = 'Odontólogo' in grupos or request.es_admin
            request.es_auxiliar = 'Auxiliar' in grupos or request.es_admin
        return self.get_response(request)
