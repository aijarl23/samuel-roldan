from django.contrib import admin
from .models import FichaClinica, EvolucionClinica, Odontograma


class EvolucionInline(admin.TabularInline):
    model = EvolucionClinica
    extra = 0
    fields = ('fecha', 'odontologo', 'procedimiento', 'dientes_tratados', 'valor_cobrado')
    readonly_fields = ('fecha',)


@admin.register(FichaClinica)
class FichaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'odontologo_principal', 'creado')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'paciente__documento')
    autocomplete_fields = ('paciente',)
    inlines = [EvolucionInline]
    readonly_fields = ('creado', 'actualizado')


@admin.register(EvolucionClinica)
class EvolucionAdmin(admin.ModelAdmin):
    list_display = ('ficha', 'odontologo', 'procedimiento', 'dientes_tratados',
                    'valor_cobrado', 'fecha', 'fecha_proxima_cita')
    list_filter = ('odontologo',)
    date_hierarchy = 'fecha'


@admin.register(Odontograma)
class OdontogramaAdmin(admin.ModelAdmin):
    list_display = ('ficha', 'odontologo', 'fecha')
