"""
Copiar a C:\\samuel_roldan\\ y ejecutar:
  python instalar_logo.py
"""
import os, shutil, base64

BASE = os.path.dirname(os.path.abspath(__file__))

# ── 1. Copiar logo a static/img/ ─────────────────────────────────────────────
img_dir = os.path.join(BASE, 'static', 'img')
os.makedirs(img_dir, exist_ok=True)

logo_hd  = os.path.join(BASE, 'logo_samuel_roldan.png')
logo_nav = os.path.join(BASE, 'logo_samuel_nav.png')

if not os.path.exists(logo_hd):
    print("ERROR: no encuentro logo_samuel_roldan.png en", BASE)
    print("Asegurate de copiar los dos archivos PNG junto a este script.")
    exit(1)

shutil.copy(logo_hd,  os.path.join(img_dir, 'logo_samuel_roldan.png'))
shutil.copy(logo_nav, os.path.join(img_dir, 'logo_samuel_nav.png'))
print("OK: logos copiados a static/img/")

# ── 2. Actualizar templates/admin/base_site.html ─────────────────────────────
admin_tpl = os.path.join(BASE, 'templates', 'admin', 'base_site.html')
os.makedirs(os.path.dirname(admin_tpl), exist_ok=True)

with open(admin_tpl, 'w', encoding='utf-8') as f:
    f.write("""{% extends "admin/base.html" %}
{% load static %}
{% block title %}{% if subtitle %}{{ subtitle }} | {% endif %}{{ title }} | Samuel Roldán{% endblock %}
{% block branding %}
<h1 id="site-name" style="display:flex;align-items:center;gap:10px;padding:6px 0;">
  <a href="{% url 'admin:index' %}" style="display:flex;align-items:center;gap:10px;text-decoration:none;">
    <img src="{% static 'img/logo_samuel_nav.png' %}" alt="Samuel Roldán" style="height:44px;width:auto;">
    <span style="color:#fff;font-size:.95rem;font-weight:600;line-height:1.2;">
      Consultorio Odontológico<br>
      <span style="font-size:.78rem;opacity:.85;font-weight:400;">Samuel Roldán · Ortodoncista</span>
    </span>
  </a>
</h1>
{% endblock %}
{% block nav_global %}{% endblock %}
{% block extrastyle %}{{ block.super }}
<style>
#header{background:linear-gradient(135deg,#0D47A1,#1565C0);padding:4px 16px;}
#header a:link,#header a:visited{color:#fff;}
.module h2,.module caption,.inline-group h2{background:#1565C0;}
div.breadcrumbs{background:#0D47A1;color:#fff;}
div.breadcrumbs a{color:rgba(255,255,255,.85);}
a:link,a:visited{color:#1565C0;}
.button,.submit-row input{background:#1565C0;border-color:#0D47A1;}
.button:hover,.submit-row input:hover{background:#0D47A1;}
#footer{background:#F4F6F9;border-top:1px solid #E0E0E0;padding:8px;text-align:center;font-size:.72rem;color:#90A4AE;}
</style>
{% endblock %}
{% block footer %}<div id="footer">Solucionar Sistemas e Ingeniería SSI &copy; {% now "Y" %}</div>{% endblock %}
""")
print("OK: templates/admin/base_site.html actualizado con logo")

# ── 3. Actualizar templates/base/base.html (navbar) ──────────────────────────
base_tpl = os.path.join(BASE, 'templates', 'base', 'base.html')

with open(base_tpl, encoding='utf-8') as f:
    contenido = f.read()

# Reemplazar el emoji por el logo real en la navbar
viejo = '<div class="brand">🦷 <span>Samuel Roldán</span></div>'
nuevo = """<div class="brand" style="display:flex;align-items:center;gap:8px;">
    <img src="/static/img/logo_samuel_nav.png" alt="Logo" style="height:38px;width:auto;">
    <span style="line-height:1.15;">Samuel Roldán<br><small style="font-size:.65rem;opacity:.8;font-weight:400;">Ortodoncista</small></span>
  </div>"""

if viejo in contenido:
    contenido = contenido.replace(viejo, nuevo)
    with open(base_tpl, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("OK: navbar actualizada con logo en templates/base/base.html")
else:
    print("AVISO: no se encontro el placeholder del logo en base.html (puede ya estar actualizado)")

print("\n✅ Logo integrado correctamente.")
print("Reinicia el servidor: python manage.py runserver 0.0.0.0:8005")
