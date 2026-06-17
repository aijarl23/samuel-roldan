"""
SOLUCION DEFINITIVA - Samuel Roldan
Logo SVG inline, sin dependencias de archivos.
Ejecutar: python FIX_DEFINITIVO.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def w(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f'  OK -> {os.path.relpath(ruta, BASE)}')

print("\n=== FIX DEFINITIVO SAMUEL ROLDAN ===\n")

SVG_AZUL = '''<svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:80px;height:80px">
  <path d="M40 10 C28 10 18 18 18 30 C18 42 22 55 26 65 C27.5 69 29 72 31 72 C33 72 34 68 35 62 C36 56 37 52 40 52 C43 52 44 56 45 62 C46 68 47 72 49 72 C51 72 52.5 69 54 65 C58 55 62 42 62 30 C62 18 52 10 40 10Z" fill="#1565C0"/>
  <rect x="36" y="24" width="8" height="20" rx="2" fill="#FB8C00"/>
  <rect x="29" y="31" width="22" height="8" rx="2" fill="#FB8C00"/>
</svg>'''

SVG_BLANCO = '''<svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:42px;height:42px;flex-shrink:0">
  <path d="M40 10 C28 10 18 18 18 30 C18 42 22 55 26 65 C27.5 69 29 72 31 72 C33 72 34 68 35 62 C36 56 37 52 40 52 C43 52 44 56 45 62 C46 68 47 72 49 72 C51 72 52.5 69 54 65 C58 55 62 42 62 30 C62 18 52 10 40 10Z" fill="white"/>
  <rect x="36" y="24" width="8" height="20" rx="2" fill="#FB8C00"/>
  <rect x="29" y="31" width="22" height="8" rx="2" fill="#FB8C00"/>
</svg>'''

# ── 1. LOGIN ──────────────────────────────────────────────────────────────────
w(os.path.join(BASE, 'templates', 'accounts', 'login.html'), f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Iniciar sesion - Samuel Roldan</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:"Segoe UI",system-ui,sans-serif;
  background:linear-gradient(135deg,#0A2E6E 0%,#1565C0 55%,#0D47A1 100%);
  min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}}
.card{{background:#fff;border-radius:20px;width:100%;max-width:420px;
  box-shadow:0 12px 40px rgba(0,0,0,.25);overflow:hidden;}}
.top{{padding:32px 28px 20px;text-align:center;border-bottom:3px solid #1565C0;
  background:linear-gradient(180deg,#F8FAFF,#fff);}}
.top h1{{color:#0D47A1;font-size:1.05rem;font-weight:700;margin:12px 0 4px;}}
.top p{{color:#607D8B;font-size:.78rem;}}
.body{{padding:26px 32px 28px;}}
.err{{background:#FFEBEE;color:#C62828;border-radius:10px;
  padding:11px 14px;font-size:.82rem;margin-bottom:16px;border-left:4px solid #C62828;}}
label{{display:block;font-size:.78rem;font-weight:600;color:#455A64;margin-bottom:6px;}}
input[type=text],input[type=password]{{width:100%;padding:13px 14px;
  border:1.5px solid #CFD8DC;border-radius:10px;font-size:.9rem;
  outline:none;transition:border .15s;margin-bottom:16px;
  touch-action:manipulation;}}
input:focus{{border-color:#1565C0;box-shadow:0 0 0 3px rgba(21,101,192,.12);}}
.btn{{width:100%;background:linear-gradient(135deg,#1565C0,#0D47A1);
  color:#fff;border:none;padding:14px;border-radius:12px;
  font-size:1rem;font-weight:700;cursor:pointer;transition:opacity .2s;
  touch-action:manipulation;letter-spacing:.3px;}}
.btn:hover{{opacity:.9;}}
.pie{{text-align:center;font-size:.65rem;color:#B0BEC5;margin-top:18px;}}
</style>
</head>
<body>
<div class="card">
  <div class="top">
    {SVG_AZUL}
    <h1>Consultorio Odontologico Samuel Roldan</h1>
    <p>Sistema de Gestion de Consentimientos Informados</p>
  </div>
  <div class="body">
    {{% if form.errors %}}
    <div class="err">&#9888; Usuario o contrasena incorrectos. Intente de nuevo.</div>
    {{% endif %}}
    <form method="post">
      {{% csrf_token %}}
      <input type="hidden" name="next" value="{{{{ next }}}}">
      <label>Usuario</label>
      <input type="text" name="username" autofocus autocomplete="username" placeholder="Ingrese su usuario">
      <label>Contrasena</label>
      <input type="password" name="password" autocomplete="current-password" placeholder="&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;&#8226;">
      <button class="btn" type="submit">Iniciar sesion &rarr;</button>
    </form>
    <div class="pie">&copy; {{% now "Y" %}} Consultorio Odontologico Samuel Roldan</div>
  </div>
</div>
</body>
</html>
''')

# ── 2. BASE.HTML ──────────────────────────────────────────────────────────────
w(os.path.join(BASE, 'templates', 'base', 'base.html'), f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>{{% block titulo %}}Panel{{% endblock %}} - Samuel Roldan</title>
<style>
:root{{
  --azul:#1565C0;--azul-osc:#0D47A1;--azul-claro:#E3F2FD;
  --naranja:#FB8C00;--verde:#2E7D32;--rojo:#C62828;
  --bg:#F0F2F5;--card:#fff;--borde:#E0E7EF;--texto:#1A237E;--sub:#546E7A;
  --sombra:0 4px 16px rgba(0,0,0,.10);--radio:14px;
}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:"Segoe UI",system-ui,sans-serif;background:var(--bg);
  color:#263238;display:flex;flex-direction:column;min-height:100vh;}}

/* NAV */
nav{{background:linear-gradient(135deg,var(--azul-osc),var(--azul));
  display:flex;align-items:center;flex-wrap:wrap;padding:0 16px;
  min-height:62px;position:sticky;top:0;z-index:200;
  box-shadow:0 2px 12px rgba(0,0,0,.18);gap:8px;}}
.nav-brand{{display:flex;align-items:center;gap:10px;text-decoration:none;padding:8px 0;}}
.nav-brand .txt{{color:#fff;line-height:1.2;}}
.nav-brand .txt strong{{font-size:.95rem;font-weight:700;}}
.nav-brand .txt span{{display:block;font-size:.68rem;color:#FB8C00;font-weight:600;}}
.nav-sp{{flex:1;}}
.nav-links{{display:flex;align-items:center;gap:4px;flex-wrap:wrap;}}
.nav-links a{{color:rgba(255,255,255,.88);text-decoration:none;font-size:.82rem;
  padding:10px 13px;border-radius:8px;transition:background .15s;
  touch-action:manipulation;white-space:nowrap;}}
.nav-links a:hover,.nav-links a.active{{background:rgba(255,255,255,.18);color:#fff;}}
.nav-user{{color:rgba(255,255,255,.6);font-size:.74rem;padding:0 6px;}}
.btn-logout{{background:rgba(255,255,255,.12);color:rgba(255,255,255,.9);border:none;
  padding:10px 13px;border-radius:8px;font-size:.82rem;cursor:pointer;
  touch-action:manipulation;transition:background .15s;}}
.btn-logout:hover{{background:rgba(255,255,255,.22);}}

/* BARRA RAPIDA */
.quickbar{{background:var(--azul-osc);padding:8px 16px;display:flex;gap:8px;
  flex-wrap:wrap;border-bottom:1px solid rgba(255,255,255,.1);}}
.qbtn{{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.12);
  color:#fff;text-decoration:none;padding:10px 16px;border-radius:10px;
  font-size:.8rem;font-weight:600;border:none;cursor:pointer;
  touch-action:manipulation;transition:background .15s;white-space:nowrap;}}
.qbtn:hover{{background:rgba(255,255,255,.22);}}
.qbtn.naranja{{background:var(--naranja);}}
.qbtn.naranja:hover{{background:#F57C00;}}

/* LAYOUT */
.page{{max-width:1220px;margin:0 auto;padding:22px 16px;flex:1;width:100%;}}

/* MENSAJES */
.msgs{{margin-bottom:16px;}}
.msg{{padding:12px 16px;border-radius:10px;font-size:.84rem;margin-bottom:6px;
  border-left:4px solid;display:flex;align-items:center;gap:8px;}}
.msg.success{{background:#E8F5E9;color:#1B5E20;border-color:#2E7D32;}}
.msg.error{{background:#FFEBEE;color:#B71C1C;border-color:#C62828;}}
.msg.warning{{background:#FFF8E1;color:#E65100;border-color:#FB8C00;}}
.msg.info{{background:var(--azul-claro);color:var(--azul-osc);border-color:var(--azul);}}

/* STATS */
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
  gap:14px;margin-bottom:22px;}}
.stat{{background:var(--card);border-radius:var(--radio);padding:20px;
  box-shadow:var(--sombra);border-top:4px solid var(--azul);
  display:flex;align-items:center;gap:14px;transition:transform .15s;}}
.stat:hover{{transform:translateY(-2px);}}
.stat.naranja{{border-top-color:var(--naranja);}}
.stat.verde{{border-top-color:var(--verde);}}
.stat.rojo{{border-top-color:var(--rojo);}}
.stat-ico{{font-size:1.8rem;width:48px;height:48px;display:flex;align-items:center;
  justify-content:center;border-radius:12px;background:var(--azul-claro);flex-shrink:0;}}
.stat.naranja .stat-ico{{background:#FFF3E0;}}
.stat.verde .stat-ico{{background:#E8F5E9;}}
.stat-num{{font-size:2rem;font-weight:800;color:var(--azul);line-height:1;}}
.stat.naranja .stat-num{{color:var(--naranja);}}
.stat.verde .stat-num{{color:var(--verde);}}
.stat-lbl{{font-size:.7rem;color:var(--sub);text-transform:uppercase;letter-spacing:.5px;margin-top:3px;}}

/* CARD */
.card{{background:var(--card);border-radius:var(--radio);box-shadow:var(--sombra);
  overflow:hidden;margin-bottom:20px;}}
.card-hdr{{padding:15px 20px;border-bottom:1px solid var(--borde);
  display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:8px;background:linear-gradient(to right,#FAFBFF,#fff);}}
.card-hdr h2{{font-size:.9rem;color:var(--azul-osc);font-weight:700;
  display:flex;align-items:center;gap:7px;}}

/* TABLA */
.t-wrap{{overflow-x:auto;}}
table{{width:100%;border-collapse:collapse;}}
th{{background:var(--azul-osc);color:#fff;padding:11px 14px;text-align:left;
  font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.4px;
  white-space:nowrap;}}
td{{padding:11px 14px;border-top:1px solid var(--borde);font-size:.83rem;
  vertical-align:middle;min-height:44px;}}
tr:hover td{{background:#F8FAFF;}}
.td-n strong{{color:var(--texto);font-size:.85rem;display:block;}}
.td-n small{{color:var(--sub);font-size:.72rem;}}

/* BADGES */
.badge{{padding:4px 11px;border-radius:20px;font-size:.68rem;font-weight:700;display:inline-block;}}
.b-pend{{background:#FFF3E0;color:#E65100;}}
.b-firm{{background:#E8F5E9;color:#2E7D32;}}
.b-bor{{background:#ECEFF1;color:#455A64;}}
.b-anul{{background:#FFEBEE;color:#C62828;}}

/* BOTONES */
.btn{{display:inline-flex;align-items:center;gap:5px;text-decoration:none;
  padding:9px 16px;border-radius:10px;font-size:.8rem;font-weight:600;
  border:none;cursor:pointer;transition:all .15s;white-space:nowrap;
  touch-action:manipulation;}}
.btn:hover{{opacity:.88;transform:translateY(-1px);}}
.btn-p{{background:var(--azul);color:#fff;}}
.btn-n{{background:var(--naranja);color:#fff;}}
.btn-v{{background:var(--verde);color:#fff;}}
.btn-g{{background:#78909C;color:#fff;}}
.btn-o{{background:transparent;color:var(--azul);border:1.5px solid var(--azul);}}
.btn-sm{{padding:5px 10px;font-size:.72rem;}}

/* BUSQUEDA */
.search-bar{{display:flex;gap:8px;flex-wrap:wrap;}}
.search-bar input{{padding:9px 13px;border:1.5px solid var(--borde);
  border-radius:10px;font-size:.83rem;outline:none;min-width:220px;
  transition:border .15s;touch-action:manipulation;}}
.search-bar input:focus{{border-color:var(--azul);}}

/* FOOTER */
footer{{text-align:center;padding:14px;font-size:.68rem;color:var(--sub);
  border-top:1px solid var(--borde);background:#fff;margin-top:auto;}}

/* RESPONSIVE TABLET */
@media(max-width:700px){{
  .nav-links a{{padding:10px 9px;font-size:.76rem;}}
  .nav-user{{display:none;}}
  .stats{{grid-template-columns:repeat(2,1fr);}}
  .quickbar{{gap:6px;}}
  .qbtn{{padding:10px 12px;font-size:.76rem;flex:1;justify-content:center;}}
  th,td{{padding:9px 10px;font-size:.78rem;}}
}}
@media(max-width:480px){{
  .nav-links a span{{display:none;}}
  .card-hdr{{flex-direction:column;align-items:flex-start;}}
}}
</style>
{{% block extra_css %}}{{% endblock %}}
</head>
<body>
<nav>
  <a class="nav-brand" href="/">
    {SVG_BLANCO}
    <div class="txt">
      <strong>Samuel Roldan</strong>
      <span>Ortodoncista</span>
    </div>
  </a>
  <div class="nav-sp"></div>
  <div class="nav-links">
    <a href="/" {{% if request.path == "/" %}}class="active"{{% endif %}}>&#127968; <span>Panel</span></a>
    <a href="/pacientes/" {{% if "/pacientes/" in request.path %}}class="active"{{% endif %}}>&#128101; <span>Pacientes</span></a>
    <a href="/admin/" target="_blank">&#9881; <span>Admin</span></a>
    <span class="nav-user">{{ request.user.get_full_name|default:request.user.username }}</span>
    <form method="post" action="/accounts/logout/" style="display:inline">
      {{% csrf_token %}}
      <button type="submit" class="btn-logout">Salir &rarr;</button>
    </form>
  </div>
</nav>

<div class="quickbar">
  <a class="qbtn naranja" href="/admin/pacientes/paciente/add/">&#43; Nuevo Paciente</a>
  <a class="qbtn" href="/">&#9998; Firmar Consentimiento</a>
  <a class="qbtn" href="/pacientes/">&#128269; Buscar Paciente</a>
</div>

<div class="page">
{{% if messages %}}
<div class="msgs">{{% for m in messages %}}
<div class="msg {{{{ m.tags }}}}">{{{{ m }}}}</div>
{{% endfor %}}</div>{{% endif %}}
{{% block contenido %}}{{% endblock %}}
</div>

<footer>&copy; {{% now "Y" %}} Consultorio Odontologico Samuel Roldan</footer>
{{% block extra_js %}}{{% endblock %}}
</body>
</html>
''')

# ── 3. ADMIN BASE_SITE ────────────────────────────────────────────────────────
w(os.path.join(BASE, 'templates', 'admin', 'base_site.html'), f'''{{% extends "admin/base.html" %}}
{{% block title %}}{{% if subtitle %}}{{{{ subtitle }}}} | {{% endif %}}{{{{ title }}}} | Samuel Roldan{{% endblock %}}
{{% block branding %}}
<h1 id="site-name" style="padding:4px 0;">
  <a href="{{% url 'admin:index' %}}"
     style="display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;">
    {SVG_BLANCO}
    <span style="font-size:.92rem;font-weight:700;line-height:1.25;color:#fff;">
      Consultorio Odontologico Samuel Roldan
      <small style="display:block;font-weight:400;font-size:.7rem;opacity:.8;color:#FB8C00;">
        Ortodoncista
      </small>
    </span>
  </a>
</h1>
{{% endblock %}}
{{% block nav_global %}}{{% endblock %}}
{{% block extrastyle %}}{{{{ block.super }}}}
<style>
#header{{background:linear-gradient(135deg,#0D47A1,#1565C0);padding:6px 16px;}}
#header a:link,#header a:visited{{color:#fff;}}
#branding h1{{margin:0;padding:0;}}
.module h2,.module caption,.inline-group h2{{background:#1565C0;}}
div.breadcrumbs{{background:#0D47A1;}}
div.breadcrumbs a{{color:rgba(255,255,255,.85);}}
a:link,a:visited{{color:#1565C0;}}
.button,input[type=submit]{{background:#1565C0 !important;border-color:#0D47A1 !important;}}
.button:hover{{background:#0D47A1 !important;}}
#footer{{text-align:center;font-size:.7rem;color:#90A4AE;padding:8px;}}
</style>
{{% endblock %}}
{{% block footer %}}
<div id="footer">&copy; {{% now "Y" %}} Consultorio Odontologico Samuel Roldan</div>
{{% endblock %}}
''')

# ── 4. PANEL mejorado ─────────────────────────────────────────────────────────
w(os.path.join(BASE, 'templates', 'base', 'panel.html'), '''\
{% extends 'base/base.html' %}
{% block titulo %}Panel Principal{% endblock %}
{% block contenido %}
<div class="stats">
  <div class="stat">
    <div class="stat-ico">&#128101;</div>
    <div><div class="stat-num">{{ total_pacientes }}</div><div class="stat-lbl">Pacientes activos</div></div>
  </div>
  <div class="stat naranja">
    <div class="stat-ico">&#9203;</div>
    <div><div class="stat-num">{{ pendientes }}</div><div class="stat-lbl">Pendientes de firma</div></div>
  </div>
  <div class="stat verde">
    <div class="stat-ico">&#9989;</div>
    <div><div class="stat-num">{{ firmados_hoy }}</div><div class="stat-lbl">Firmados hoy</div></div>
  </div>
  <div class="stat">
    <div class="stat-ico">&#128196;</div>
    <div><div class="stat-num">{{ firmados_mes }}</div><div class="stat-lbl">Este mes</div></div>
  </div>
</div>

{% if pendientes_lista %}
<div class="card">
  <div class="card-hdr">
    <h2>&#9889; Pendientes de firma</h2>
    <a class="btn btn-n" href="/admin/consentimientos/consentimiento/add/">+ Nuevo consentimiento</a>
  </div>
  <div class="t-wrap">
  <table>
    <tr><th>Paciente</th><th>Procedimiento</th><th>Creado</th><th>Accion</th></tr>
    {% for c in pendientes_lista %}
    <tr>
      <td><div class="td-n"><strong>{{ c.paciente.nombre_completo }}</strong><small>{{ c.paciente.tipo_documento }} {{ c.paciente.documento }}</small></div></td>
      <td>{{ c.plantilla.nombre }}</td>
      <td>{{ c.creado|date:"d/m/Y H:i" }}</td>
      <td><a class="btn btn-n btn-sm" href="/consentimientos/firmar/{{ c.id }}/">&#9998; Firmar ahora</a></td>
    </tr>
    {% endfor %}
  </table>
  </div>
</div>
{% endif %}

<div class="card">
  <div class="card-hdr">
    <h2>&#128203; Consentimientos recientes</h2>
    <a class="btn btn-o btn-sm" href="/pacientes/">Ver todos los pacientes &rarr;</a>
  </div>
  <div class="t-wrap">
  <table>
    <tr><th>Paciente</th><th>Procedimiento</th><th>Odontologo</th><th>Estado</th><th>Fecha</th><th>Acciones</th></tr>
    {% for c in recientes %}
    <tr>
      <td><div class="td-n"><strong>{{ c.paciente.nombre_completo }}</strong><small>{{ c.paciente.documento }}</small></div></td>
      <td>{{ c.plantilla.tipo }}</td>
      <td>{{ c.odontologo.get_full_name|default:c.odontologo.username }}</td>
      <td>
        {% if c.estado == 'PENDIENTE' %}<span class="badge b-pend">&#9203; Pendiente</span>
        {% elif c.estado == 'FIRMADO' %}<span class="badge b-firm">&#9989; Firmado</span>
        {% elif c.estado == 'BORRADOR' %}<span class="badge b-bor">Borrador</span>
        {% else %}<span class="badge b-anul">Anulado</span>{% endif %}
      </td>
      <td style="white-space:nowrap">{{ c.fecha_firma|default:c.creado|date:"d/m/Y H:i" }}</td>
      <td style="white-space:nowrap">
        {% if c.estado == 'PENDIENTE' %}<a class="btn btn-n btn-sm" href="/consentimientos/firmar/{{ c.id }}/">&#9998;</a>{% endif %}
        {% if c.pdf %}<a class="btn btn-p btn-sm" href="/consentimientos/{{ c.id }}/pdf/" target="_blank">&#128196;</a>{% endif %}
        <a class="btn btn-o btn-sm" href="/consentimientos/{{ c.id }}/">Ver</a>
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="6" style="text-align:center;padding:32px;color:#90A4AE;">
      Sin consentimientos aun. <a href="/admin/consentimientos/consentimiento/add/">Crear el primero</a>
    </td></tr>
    {% endfor %}
  </table>
  </div>
</div>
{% endblock %}
''')

print("\n=== LISTO ===")
print("Reinicia el servidor:")
print("  python manage.py runserver 0.0.0.0:8005")
