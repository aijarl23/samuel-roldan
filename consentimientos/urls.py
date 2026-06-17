from django.urls import path
from . import views

app_name = 'consentimientos'
urlpatterns = [
    path('firmar/<int:pk>/', views.firmar, name='firmar'),
    path('<int:pk>/', views.detalle, name='detalle'),
    path('<int:pk>/pdf/', views.ver_pdf, name='pdf'),
    path('paciente/<int:paciente_pk>/', views.lista_paciente, name='lista_paciente'),
]
