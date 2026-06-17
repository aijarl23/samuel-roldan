
from django.contrib import admin
from django.utils.html import mark_safe
from .models import PlantillaConsentimiento, Consentimiento


@admin.register(PlantillaConsentimiento)
class PlantillaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'version', 'requiere_autorizacion_expediente', 'activa')
    list_filter = ('tipo', 'activa')
    search_fields = ('nombre',)
    readonly_fields = ('creado', 'actualizado')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Consentimiento)
class ConsentimientoAdmin(admin.ModelAdmin):
    list_display  = ('paciente', 'plantilla', 'odontologo', 'estado_col',
                     'fecha_firma', 'enviado_correo', 'acciones')
    list_filter   = ('estado', 'plantilla__tipo', 'odontologo', 'enviado_correo')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'paciente__documento')
    autocomplete_fields = ('paciente',)
    date_hierarchy = 'creado'
    list_per_page  = 25
    readonly_fields = (
        'texto_generado', 'fecha_firma', 'ip_firma', 'dispositivo',
        'hash_documento', 'drive_url', 'firma_paciente', 'firma_acudiente',
        'enviado_correo', 'enviado_whatsapp', 'fecha_envio_correo',
        'fecha_envio_whatsapp', 'creado', 'creado_por',
    )

    COLS = {
        'BORRADOR': ('gray',    'Borrador'),
        'PENDIENTE': ('#E65100','Pendiente'),
        'FIRMADO':   ('#2E7D32','Firmado'),
        'ANULADO':   ('#C62828','Anulado'),
    }

    def get_fields(self, request, obj=None):
        if obj is None:
            return ('paciente', 'plantilla', 'odontologo', 'notas_internas')
        return (
            'paciente', 'plantilla', 'odontologo', 'estado', 'notas_internas',
            'autoriza_expediente', 'fecha_firma', 'ip_firma', 'dispositivo',
            'hash_documento', 'drive_url',
            'enviado_correo', 'fecha_envio_correo',
            'enviado_whatsapp', 'fecha_envio_whatsapp',
            'creado', 'creado_por',
        )

    def estado_col(self, obj):
        color, label = self.COLS.get(obj.estado, ('#000', obj.estado))
        return mark_safe(f'<b style="color:{color}">{label}</b>')
    estado_col.short_description = 'Estado'

    def acciones(self, obj):
        bts = []
        if obj.estado == 'PENDIENTE':
            bts.append(f'<a class="button" href="/consentimientos/firmar/{obj.id}/">Firmar</a>')
        if obj.pdf:
            bts.append(f'<a class="button" href="/consentimientos/{obj.id}/pdf/" target="_blank">PDF</a>')
        if obj.drive_url:
            bts.append(f'<a class="button" href="{obj.drive_url}" target="_blank">Drive</a>')
        return mark_safe(' '.join(bts)) if bts else mark_safe('-')
    acciones.short_description = ''

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
