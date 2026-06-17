"""
Ejecutar en C:\\samuel_roldan con el venv activo:
  python fix_samuel.py
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def leer(f):
    with open(f, encoding='utf-8') as fh:
        return fh.read()

def escribir(f, content):
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print(f'  OK: {f}')

# ── 1. settings/base.py: quitar jazzmin ─────────────────────────────────────
p = os.path.join(BASE, 'config', 'settings', 'base.py')
txt = leer(p)
txt = txt.replace("    'jazzmin',\n", "")
txt = txt.replace("    'jazzmin',", "")
# Quitar JAZZMIN_SETTINGS y JAZZMIN_UI_TWEAKS completos
import re
txt = re.sub(r"\nJAZZMIN_SETTINGS\s*=\s*\{.*?\n\}\n", "\n", txt, flags=re.DOTALL)
txt = re.sub(r"\nJAZZMIN_UI_TWEAKS\s*=\s*\{.*?\n\}\n", "\n", txt, flags=re.DOTALL)
# Quitar custom_css que depende de jazzmin
txt = txt.replace("    'custom_css': 'css/admin_extra.css',\n", "")
escribir(p, txt)

# ── 2. Reemplazar admin base con tema propio simple ──────────────────────────
admin_base = os.path.join(BASE, 'templates', 'admin', 'base_site.html')
os.makedirs(os.path.dirname(admin_base), exist_ok=True)
escribir(admin_base, """{% extends "admin/base.html" %}
{% block title %}{% if subtitle %}{{ subtitle }} | {% endif %}{{ title }} | Samuel Roldán{% endblock %}
{% block branding %}
<h1 id="site-name">
  <a href="{% url 'admin:index' %}">&#x1F9B7; Consultorio Odontológico Samuel Roldán</a>
</h1>
{% endblock %}
{% block nav_global %}{% endblock %}
{% block extrastyle %}{{ block.super }}
<style>
#header{background:linear-gradient(135deg,#0D47A1,#1565C0);color:#fff;}
#header a:link,#header a:visited{color:#fff;}
#branding h1{color:#fff;font-size:1.1rem;}
#branding h1 a{color:#fff;}
.module h2,.module caption,.inline-group h2{background:#1565C0;}
div.breadcrumbs{background:#0D47A1;color:#fff;}
div.breadcrumbs a{color:rgba(255,255,255,.8);}
a:link,a:visited{color:#1565C0;}
.button,.submit-row input{background:#1565C0;border-color:#0D47A1;}
.button:hover,.submit-row input:hover{background:#0D47A1;}
#footer{background:#F4F6F9;border-top:1px solid #E0E0E0;padding:10px;text-align:center;font-size:.75rem;color:#90A4AE;}
</style>
{% endblock %}
{% block footer %}<div id="footer">Solucionar Sistemas e Ingeniería SSI &copy; {% now "Y" %}</div>{% endblock %}
""")

# ── 3. Verificar que manage.py usa development settings ──────────────────────
mp = os.path.join(BASE, 'manage.py')
txt_mp = leer(mp)
if 'development' not in txt_mp:
    txt_mp = txt_mp.replace(
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')",
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')"
    )
    escribir(mp, txt_mp)

print("\n✅ Fix aplicado. Ahora ejecuta:")
print("   python manage.py runserver 0.0.0.0:8005")
