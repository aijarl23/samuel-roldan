from django.urls import path
from . import views

app_name = 'historial'
urlpatterns = [
    path('paciente/<int:paciente_pk>/', views.ficha, name='ficha'),
]
