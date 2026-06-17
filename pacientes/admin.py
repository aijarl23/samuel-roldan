
from django.contrib import admin
from django.utils.html import mark_safe
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display  = ('nombre_completo', 'tipo_documento', 'documento', 'edad',
                     'telefono', 'correo', 'es_menor', 'activo', 'acciones')
    list_filter   = ('tipo_documento', 'sexo', 'es_menor', 'activo', 'ciudad')
    search_fields = ('nombres', 'apellidos', 'documento', 'correo', 'telefono')
    list_per_page = 25
    date_hierarchy = 'creado'
    readonly_fields = ('creado', 'actualizado')
    fieldsets = (
        ('Identificacion', {'fields': (
            ('tipo_documento', 'documento'),
            ('nombres', 'apellidos'),
            ('fecha_nacimiento', 'sexo', 'grupo_sanguineo'),
            'foto', 'activo',
        )}),
        ('Contacto', {'fields': (
            ('telefono', 'correo'), 'direccion', 'ciudad', 'eps', 'ocupacion',
        )}),
        ('Acudiente (menor de edad)', {'classes': ('collapse',), 'fields': (
            'es_menor',
            ('acudiente_nombre', 'acudiente_parentesco'),
            ('acudiente_tipo_doc', 'acudiente_documento', 'acudiente_telefono'),
        )}),
        ('Antecedentes medicos', {'classes': ('collapse',), 'fields': (
            'alergias', 'medicamentos', 'antecedentes', 'observaciones',
        )}),
        ('Auditoria', {'classes': ('collapse',), 'fields': ('creado', 'actualizado')}),
    )

    def acciones(self, obj):
        return mark_safe(
            f'<a class="button" href="/historial/paciente/{obj.pk}/">Historia</a> '
            f'<a class="button" href="/consentimientos/paciente/{obj.pk}/">Consent.</a>'
        )
    acciones.short_description = ''
