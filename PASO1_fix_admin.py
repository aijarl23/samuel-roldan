"""
Ejecutar en C:\\samuel_roldan con venv activo:
  python PASO1_fix_admin.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def w(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f'  OK -> {os.path.relpath(ruta, BASE)}')

print("\n=== APLICANDO FIXES SAMUEL ROLDAN ===\n")

# ── 1. consentimientos/admin.py — fix TypeError ───────────────────────────────
w(os.path.join(BASE, 'consentimientos', 'admin.py'), """
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
""")

# ── 2. pacientes/admin.py — fix format_html ───────────────────────────────────
w(os.path.join(BASE, 'pacientes', 'admin.py'), """
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
""")

# ── 3. Logout POST en base.html ───────────────────────────────────────────────
base_tpl = os.path.join(BASE, 'templates', 'base', 'base.html')
try:
    with open(base_tpl, encoding='utf-8') as f:
        txt = f.read()
    if '<a href="/accounts/logout/">Salir</a>' in txt:
        txt = txt.replace(
            '<a href="/accounts/logout/">Salir</a>',
            '''<form method="post" action="/accounts/logout/" style="display:inline">
      {% csrf_token %}
      <button type="submit" style="background:rgba(255,255,255,.15);color:#fff;border:none;padding:6px 12px;border-radius:6px;font-size:.82rem;cursor:pointer;">Salir</button>
    </form>'''
        )
        with open(base_tpl, 'w', encoding='utf-8') as f:
            f.write(txt)
        print('  OK -> logout corregido en base.html')
    else:
        print('  INFO -> logout ya estaba corregido')
except FileNotFoundError:
    print('  AVISO -> base.html no encontrado, omitiendo')

# ── 4. Admin base con colores (sin jazzmin) ───────────────────────────────────
w(os.path.join(BASE, 'templates', 'admin', 'base_site.html'), """{% extends "admin/base.html" %}
{% block title %}{% if subtitle %}{{ subtitle }} | {% endif %}{{ title }} | Samuel Roldan{% endblock %}
{% block branding %}
<h1 id="site-name">
  <a href="{% url 'admin:index' %}" style="color:#fff;text-decoration:none;font-size:.95rem;font-weight:700;">
    &#x1F9B7; Consultorio Odontologico Samuel Roldan
  </a>
</h1>
{% endblock %}
{% block nav_global %}{% endblock %}
{% block extrastyle %}{{ block.super }}
<style>
#header{background:linear-gradient(135deg,#0D47A1,#1565C0);padding:8px 16px;}
#header a:link,#header a:visited{color:#fff;}
.module h2,.module caption,.inline-group h2{background:#1565C0;}
div.breadcrumbs{background:#0D47A1;}
div.breadcrumbs a{color:rgba(255,255,255,.85);}
a:link,a:visited{color:#1565C0;}
.button,input[type=submit]{background:#1565C0 !important;border-color:#0D47A1 !important;}
.button:hover{background:#0D47A1 !important;}
#footer{text-align:center;font-size:.7rem;color:#90A4AE;padding:8px;}
</style>
{% endblock %}
{% block footer %}<div id="footer">Solucionar Sistemas e Ingenieria SSI &copy; {% now "Y" %}</div>{% endblock %}
""")

print("\n=== LISTO ===")
print("Reinicia el servidor:")
print("  python manage.py runserver 0.0.0.0:8005")
print("\nLuego ve a: http://localhost:8005/admin/consentimientos/consentimiento/")
print("El error TypeError ya no debe aparecer.")
