from django.conf import settings


def globals(request):
    return {
        'SITE_NAME': 'Consultorio Odontológico Samuel Roldán',
        'SSI_BRAND': 'Solucionar Sistemas e Ingeniería SSI',
        'es_admin': getattr(request, 'es_admin', False),
        'es_odontologo': getattr(request, 'es_odontologo', False),
        'es_auxiliar': getattr(request, 'es_auxiliar', False),
    }
