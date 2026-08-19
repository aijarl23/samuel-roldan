from django.urls import path
from . import views

app_name = 'pacientes'
urlpatterns = [
    path('', views.lista, name='lista'),
    path('buscar-json/', views.buscar_json, name='buscar_json'),
    path('nuevo/panel/', views.crear_panel, name='crear_panel'),
    path('<int:pk>/', views.detalle, name='detalle'),
]
