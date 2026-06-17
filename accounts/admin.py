from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'tarjeta_profesional', 'telefono')
    list_filter = ('rol',)
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')
