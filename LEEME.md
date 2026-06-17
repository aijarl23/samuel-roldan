# Sistema de Gestión Odontológica — Consultorio Samuel Roldán
**Desarrollado por Solucionar Sistemas e Ingeniería SSI**

## Arquitectura (mejores prácticas Django)
```
config/
  settings/
    base.py          → Configuración compartida
    development.py   → Desarrollo (SQLite, consola de correo)
    production.py    → Producción (PostgreSQL, HTTPS, email SMTP)
  middleware.py      → Login obligatorio + contexto de rol
  context_processors.py → Variables globales en templates
accounts/            → Perfiles y autenticación
pacientes/           → Gestión de pacientes
consentimientos/
  models.py          → Consentimiento con hash de integridad
  views.py           → Panel, firma táctil, detalle, PDF
  services/
    pdf.py           → PDF profesional con ReportLab (funciona en Windows)
    drive.py         → Subida organizada a Google Drive
    notificaciones.py → Email + WhatsApp (Twilio)
historial/           → Ficha clínica, evoluciones, odontograma
templates/           → UI responsiva sin dependencias externas
```

## Instalación en Windows (primera vez)
```powershell
cd C:\samuel_roldan
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python setup_inicial.py
python manage.py runserver 0.0.0.0:8005
```
Acceder: http://localhost:8005/
Usuario: **admin** · Clave: **SamuelRoldan2026!**
**Cambiar la clave al primer ingreso** (Admin → Usuarios → admin → Cambiar contraseña)

## Flujo de trabajo
1. Auxiliar registra paciente: /admin/pacientes/paciente/add/
2. Crea consentimiento: /admin/consentimientos/consentimiento/add/
   (elige paciente, plantilla de procedimiento, odontólogo)
3. En el panel, clic "✍ Firmar ahora" → pasar tablet/celular al paciente
4. Paciente firma con el dedo, marca SÍ/NO expediente, confirma
5. Sistema genera PDF, lo guarda y (si está configurado) sube a Drive y envía correo/WhatsApp

## Roles
| Rol | Acceso |
|---|---|
| Administrador | Todo el sistema + configuración + auditoría |
| Odontólogo | Pacientes, consentimientos, firma, historia clínica |
| Auxiliar | Registro de pacientes y gestión de firmas (sin eliminar) |

Crear usuarios: Admin → Usuarios → "Agregar usuario" → asignar grupo (rol).

## Google Drive (opcional — configurar cuando esté listo)
1. Google Cloud Console → crear proyecto → habilitar Drive API
2. Crear cuenta de servicio → descargar JSON → guardar como `credenciales_drive.json`
3. Compartir la carpeta institucional de Drive con el correo de la cuenta de servicio
4. En `.env`: `GOOGLE_DRIVE_FOLDER_ID=ID_de_la_carpeta_raiz`
Sin esto configurado el sistema funciona normalmente y guarda los PDF en `/media/`.
Estructura en Drive: `Raiz / Año / Mes / CC-ApellidoNombre / archivo.pdf`

## Variables de entorno (.env)
Copiar `.env.example` a `.env` y completar antes de desplegar en producción.
Las claves sensibles NUNCA van en el código fuente.

## Plantillas incluidas
- Ortodoncia (texto extraído del formulario físico del consultorio)
- Endodoncia
- Exodoncia
Agregar más: Admin → Plantillas de consentimiento → Agregar

## Despliegue en Railway (producción)
```
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=<clave-segura>
DATABASE_URL=<postgres-url>
ALLOWED_HOSTS=tu-app.up.railway.app
```

## Pendiente Fase 3
- Recordatorios automáticos de citas
- Multi-consultorio (SaaS para revender)
- Odontograma visual interactivo
- Portal de pacientes para ver sus documentos
- Estadísticas y reportes de procedimientos

---
*Versión 2.0 — Junio 2026 · Solucionar Sistemas e Ingeniería SSI*
