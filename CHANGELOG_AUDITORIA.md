# CHANGELOG — Rediseño Clínica R
Registro técnico de todos los cambios implementados en esta sesión, en orden de ejecución. Cada módulo fue verificado antes de continuar al siguiente (local, con Django test client — ver `verificacion_e2e.py`).

---

## Módulo 0 — Blindaje (bug crítico de la auditoría previa)
**Archivo:** `templates/consentimientos/firmar.html`
**Cambio:** `{% if c.plantilla.requiere_autorización_expediente %}` → `{% if c.plantilla.requiere_autorizacion_expediente %}` (sin tilde, coincide con el campo real del modelo).
**Efecto:** la casilla legal "Autorización para uso del expediente" ahora sí aparece al firmar cuando la plantilla lo requiere. Antes se evaluaba silenciosamente como falso y nunca se mostraba.
**Verificado:** `grep` exhaustivo confirma 0 tildes restantes dentro de variables Django en todo `/templates`.

## Módulo 1 — Sistema de diseño base
**Archivos nuevos:**
- `static/css/tokens.css` — paleta de marca, tipografía, espaciado, radios, sombras (variables CSS).
- `static/css/components.css` — botones, tarjetas, badges, formularios, tablas, toasts, modales, drawer, stepper.
- `static/css/layout.css` — barra superior, grillas, estructura de la Ficha del Paciente, login.
- `templates/base/_logo.html` — logo de Clínica R como SVG vectorial (monograma "R" + arco de puntos), reutilizable con color y tamaño parametrizables.

**Nota técnica:** el logo se reconstruyó como SVG en vez de extraer un raster del PDF de marca, porque las imágenes embebidas en el PDF no tenían capa de transparencia utilizable (máscaras separadas del color). El SVG escala perfecto en cualquier tamaño y usa exactamente los colores de la paleta definida.

## Módulo 2 — Capa de navegación
**Archivos modificados:** `templates/base/base.html` (barra superior con buscador en vivo + botón de nuevo paciente + menú de usuario), `templates/accounts/login.html` (pantalla de login con la nueva identidad).
**Archivos nuevos:** `templates/base/_toast.html` (mensajes de Django convertidos en toasts visuales, mismo backend de `django.contrib.messages`, sin cambios de lógica), `static/js/drawer.js` (paneles laterales genéricos reutilizables), `static/js/buscador.js` (autocompletado del buscador global).

## Módulo 3 — Buscador de pacientes en vivo
**Archivo modificado:** `pacientes/views.py` — nueva vista `buscar_json` (no toca `lista` ni `detalle` existentes).
**Archivo modificado:** `pacientes/urls.py` — nueva ruta `pacientes/buscar-json/`.
**Verificado:** búsqueda por nombre/documento devuelve resultados correctos vía JSON, incluye conteo de consentimientos pendientes por paciente.

## Módulo 4 — Creación de paciente sin pasar por el admin
**Archivos nuevos:** `pacientes/forms.py` (`PacienteRapidoForm`, formulario corto con validación de datos de acudiente cuando `es_menor=True`), `templates/pacientes/_crear_panel.html` (fragmento para el drawer).
**Archivo modificado:** `pacientes/views.py` — nueva vista `crear_panel` (GET muestra formulario, POST vía AJAX crea el paciente y devuelve la URL de su Ficha).
**Archivo modificado:** `pacientes/urls.py` — nueva ruta `pacientes/nuevo/panel/`.
**Verificado:** paciente adulto y paciente menor (con datos de acudiente) se crean correctamente; validación exige acudiente cuando `es_menor` está marcado.

## Módulo 5 — Ficha del Paciente (pantalla central)
**Archivo modificado:** `pacientes/views.py` — vista `detalle` ampliada para incluir un resumen de historia clínica (ficha clínica + últimas 5 evoluciones) y las plantillas de consentimiento activas, sin romper `/historial/paciente/<pk>/` que sigue existiendo para el detalle completo.
**Archivo modificado:** `templates/pacientes/detalle.html` — rediseño completo: datos del paciente, consentimientos (con acciones de firmar/ver PDF), resumen de historia clínica, todo en una sola pantalla con scroll, sin pestañas ocultas.

## Módulo 6 — Asistente de consentimiento (drawer, 3 pasos)
**Archivo nuevo:** `templates/consentimientos/_asistente_panel.html` — Paso 1 del asistente (elegir tipo de consentimiento entre las plantillas activas).
**Archivo modificado:** `consentimientos/views.py` — nueva vista `asistente`: crea el `Consentimiento` en estado `PENDIENTE` y entrega la URL de la vista `firmar` **ya existente** — decisión de diseño deliberada: la captura de firma, generación de PDF, hash y notificaciones **no se duplican en ningún momento**, se reutiliza el código probado tal cual.
**Archivo modificado:** `consentimientos/urls.py` — nueva ruta `consentimientos/asistente/<paciente_pk>/`.
**Decisión documentada:** el odontólogo que firma el consentimiento (`campo odontologo`) se asigna automáticamente como el usuario que crea el consentimiento (`request.user`). Si en el futuro varios odontólogos usan la misma cuenta o se requiere selección manual, esto es un cambio de una línea en `asistente()` — señalado aquí para que quede explícito, no es una limitación oculta.

## Módulo 7 — Pantalla de firma rediseñada
**Archivo modificado:** `templates/consentimientos/firmar.html` — rediseño visual completo (stepper, tarjetas, texto legal en contenedor con scroll propio, badges). **Los IDs y atributos `name` de los campos de firma (`canvas-paciente`, `firma-paciente`, `canvas-acudiente`, `firma-acudiente`, `autoriza_expediente`) se preservaron exactamente iguales** porque la vista `firmar()` en `consentimientos/views.py` los lee por nombre — cambiar cualquiera de ellos habría roto la captura de firma sin que fuera evidente hasta producción. El JavaScript de captura del `<canvas>` es el mismo mecanismo original, solo se le cambió el color del trazo para que combine con la paleta nueva.
**Verificado:** firma de paciente solo (adulto) → `FIRMADO`; firma de paciente sin firma de acudiente en menor → sigue `PENDIENTE` (rechazo correcto, lógica de backend intacta); firma de paciente + acudiente en menor → `FIRMADO`. PDF se genera, hash SHA-256 se calcula, descarga responde con un PDF válido (`%PDF` en los primeros bytes).

## Módulo 8 — Pantallas secundarias
**Archivos modificados:** `templates/consentimientos/detalle.html`, `templates/pacientes/lista.html` — rediseño visual con el sistema de componentes nuevo, sin cambios de lógica ni de contexto de vista.

## Módulo 9 — Identidad visual del panel de administración
**Archivo modificado:** `templates/admin/base_site.html` — solo colores de acento (de azul a la paleta verde de Clínica R) y el nombre de marca en el encabezado. La estructura de bloques (`{% block branding %}`, `{% block extrastyle %}`, `{% block footer %}`) se mantuvo intacta, respetando la regla ya documentada de no sobrescribir este archivo de forma destructiva.

## Módulo 10 — Nuevas plantillas de consentimiento
**Archivo nuevo:** `consentimientos/management/commands/cargar_plantillas_clinica_r.py` — comando de gestión (no una migración de Django) que:
1. Desactiva las plantillas de consentimiento actualmente activas (`activa=False`), **sin borrar ninguna fila**.
2. Crea dos plantillas nuevas y activas con el texto legal completo, verbatim, extraído de tus archivos:
   - **"Ortodoncia — Consentimiento General (Alineadores, Brackets y auxiliares)"** — de `Consentimiento_Informado_todos__V_4_2.docx`.
   - **"Ortodoncia Interceptiva — Tratamiento Temprano"** — de `Consentimiento_Informado_tto_temprano_V1_011.docx`.

El texto se extrajo con la herramienta de extracción de documentos (no transcripción manual) y se recortó únicamente la sección final de firmas de ejemplo ya diligenciadas (nombre, cédula y fecha de una paciente real que aparecía como ilustración en el `.docx` de origen) — esa sección no es texto legal reutilizable, es el bloque de firma que el sistema ya genera dinámicamente con el canvas táctil.

**Por qué no es una migración de Django:** ejecutar esto es una decisión tuya, explícita, en el momento que elijas (no se dispara sola al desplegar). Es reversible: basta con reactivar la plantilla anterior desde el admin si hace falta.

**Cómo ejecutarlo (tú decides cuándo):**
```powershell
cd C:\samuel_roldan
.\venv\Scripts\python.exe manage.py cargar_plantillas_clinica_r --dry-run   # revisa qué haría, sin escribir nada
.\venv\Scripts\python.exe manage.py cargar_plantillas_clinica_r             # lo ejecuta de verdad
```

**Verificado en este entorno de pruebas:** plantilla antigua de prueba quedó `activa=False` (conservada); las 2 nuevas quedaron `activa=True` con el texto legal completo (13.053 y 13.462 caracteres respectivamente). Un consentimiento ya firmado con la plantilla antigua **no pudo ser borrado** por la protección `on_delete=PROTECT` del modelo — confirma que la trazabilidad legal está garantizada por el diseño ya existente del sistema, sin necesidad de ninguna acción adicional.

---

## Qué NO se tocó (verificado explícitamente)

- Modelos, migraciones, esquema de base de datos: sin cambios.
- `consentimientos/services/pdf.py` (ReportLab), `services/drive.py`, `services/notificaciones.py`: sin cambios de una sola línea.
- Middleware de autenticación y roles (`LoginRequiredMiddleware`, `RoleContextMiddleware`): sin cambios.
- Lógica de captura de firma, cálculo de hash, generación de PDF: sin cambios — solo reutilizada.
- URLs existentes: ninguna se eliminó, solo se añadieron nuevas.
- Panel de administración de Django: sigue operativo, solo con acentos de color nuevos.

## Verificación realizada en este entorno de pruebas

Ver `verificacion_e2e.py` (script de verificación de esta sesión, no forma parte del código de producción del proyecto). Resultado: **25/25 verificaciones pasaron**, cubriendo: login, carga de CSS/JS estáticos, creación de paciente (adulto y menor con acudiente), buscador en vivo, asistente de consentimiento, firma con una y dos firmas requeridas, rechazo correcto de firma incompleta, generación de PDF y hash, descarga de PDF válido, trazabilidad de texto congelado, y que el admin de Django sigue respondiendo 200.

## Pendiente de tu parte antes de ir a producción

1. **Ejecutar el comando de plantillas** (`cargar_plantillas_clinica_r`) en tu entorno local primero, revisar en el admin que el texto se vea correcto, y solo después en Railway.
2. **Confirmar los hex exactos de la paleta** si tienes el archivo fuente de diseño — actualmente uso los valores extraídos visualmente del PDF de marca (documentado en `REDISEÑO_COMPLETO_CLINICA_R.md`, sección 4.1).
3. Probar visualmente en tu navegador real (tablet/celular) — mi verificación fue funcional (backend/HTTP), no pixel-perfect visual en todos los tamaños de pantalla.
