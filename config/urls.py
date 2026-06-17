from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from consentimientos.views import panel

admin.site.site_header = 'Consultorio Odontológico Samuel Roldán'
admin.site.site_title = 'Samuel Roldán'
admin.site.index_title = 'Panel de administración'

urlpatterns = [
    path('', panel, name='panel'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('pacientes/', include('pacientes.urls', namespace='pacientes')),
    path('consentimientos/', include('consentimientos.urls', namespace='consentimientos')),
    path('historial/', include('historial.urls', namespace='historial')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
