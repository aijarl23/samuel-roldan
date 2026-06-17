import os

BASE = r'C:\samuel_roldan'
ruta = os.path.join(BASE, 'templates', 'accounts', 'login.html')

html = """\
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Iniciar sesion - Samuel Roldan</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0A2E6E 0%,#1565C0 55%,#0D47A1 100%);
  min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}
.card{background:#fff;border-radius:20px;width:100%;max-width:400px;
  box-shadow:0 12px 40px rgba(0,0,0,.25);overflow:hidden;}
.top{padding:28px 28px 16px;text-align:center;border-bottom:3px solid #1565C0;}
.top img{height:130px;width:auto;margin-bottom:10px;}
.top h1{color:#0D47A1;font-size:1rem;font-weight:700;margin-bottom:2px;}
.top p{color:#607D8B;font-size:.75rem;}
.body{padding:24px 32px 28px;}
.err{background:#FFEBEE;color:#C62828;border-radius:8px;
  padding:10px 14px;font-size:.8rem;margin-bottom:14px;border-left:4px solid #C62828;}
label{display:block;font-size:.78rem;font-weight:600;color:#455A64;margin-bottom:5px;}
input[type=text],input[type=password]{width:100%;padding:11px 14px;
  border:1.5px solid #CFD8DC;border-radius:9px;font-size:.88rem;
  outline:none;transition:border .15s;margin-bottom:14px;}
input:focus{border-color:#1565C0;box-shadow:0 0 0 3px rgba(21,101,192,.1);}
.btn{width:100%;background:linear-gradient(135deg,#1565C0,#0D47A1);
  color:#fff;border:none;padding:13px;border-radius:10px;
  font-size:.95rem;font-weight:700;cursor:pointer;}
.btn:hover{opacity:.9;}
.pie{text-align:center;font-size:.63rem;color:#B0BEC5;margin-top:16px;}
</style>
</head>
<body>
<div class="card">
  <div class="top">
    <img src="/static/img/logo_hd.png" alt="Samuel Roldan Ortodoncista">
    <h1>Consultorio Odontologico Samuel Roldan</h1>
    <p>Sistema de Gestion de Consentimientos Informados</p>
  </div>
  <div class="body">
    {% if form.errors %}
    <div class="err">Usuario o contrasena incorrectos. Intente de nuevo.</div>
    {% endif %}
    <form method="post">
      {% csrf_token %}
      <input type="hidden" name="next" value="{{ next }}">
      <label>Usuario</label>
      <input type="text" name="username" autofocus autocomplete="username" placeholder="Ingrese su usuario">
      <label>Contrasena</label>
      <input type="password" name="password" autocomplete="current-password" placeholder="........">
      <button class="btn" type="submit">Iniciar sesion</button>
    </form>
    <div class="pie">Solucionar Sistemas e Ingenieria SSI</div>
  </div>
</div>
</body>
</html>
"""

with open(ruta, 'w', encoding='utf-8') as f:
    f.write(html)
print('OK - login.html actualizado')
print('Recarga el navegador con Ctrl+Shift+R')
