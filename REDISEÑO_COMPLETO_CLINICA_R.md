# REDISEÑO COMPLETO — Clínica R (Samuel Roldán)
**Fecha:** 27/07/2026 | **Estado:** Propuesta — pendiente de tu aprobación
**Cero código todavía. Este documento reemplaza y profundiza el plan anterior.**

---

## 0. Cómo trabaja realmente un odontólogo en consulta (punto de partida del diseño)

Antes de diseñar pantallas, esto es lo que determina cada decisión de UX:

- Tiene al paciente **en la silla, en tiempo real**. No puede perder tiempo navegando.
- Usa **una mano** frecuentemente (guantes, instrumentos cerca) — objetivos de toque grandes, poco scroll horizontal, nada que dependa de doble clic o combinaciones de teclas.
- Necesita **una sola pantalla de referencia** por paciente: no quiere saltar entre 4 vistas para saber su historia, firmar un consentimiento y ver el PDF anterior.
- El momento de firma es **con el paciente mirando la pantalla** — la interfaz de firma debe verse profesional y confiable, no como un formulario administrativo.
- Trabaja en **tablet o portátil**, a veces con luz de consultorio variable — alto contraste, texto legible sin acercarse.
- Odia los **mensajes de error genéricos** ("Ha ocurrido un error") — necesita saber exactamente qué falta.

Consecuencia directa de diseño: **la Ficha del Paciente es el centro de gravedad de todo el sistema.** Todo lo demás (buscar, crear paciente) existe solo para llegar ahí lo más rápido posible.

---

## 1. Mapa de navegación

```
┌─────────────────────────────────────────────────────────┐
│  BARRA SUPERIOR (persistente en todo el sistema)          │
│  Logo Clínica R | Buscador global de paciente | Usuario   │
└─────────────────────────────────────────────────────────┘
        │
        ├── PANEL (inicio)
        │     · Métricas del día (pendientes, firmados hoy/mes)
        │     · Resultados de búsqueda reciente
        │     · Botón único: "Buscar o crear paciente"
        │
        ├── FICHA DEL PACIENTE  ← pantalla central del sistema
        │     · Datos del paciente (editable inline)
        │     · Historia clínica (resumen + evoluciones)
        │     · Consentimientos (lista + estado + acciones)
        │     · Acción: Nuevo consentimiento (abre panel lateral, no navega)
        │     · Acción: Firmar (abre panel lateral, no navega)
        │     · Acción: Ver/descargar PDF (abre en la misma pantalla)
        │
        ├── CREAR PACIENTE (modal/panel, no pantalla completa)
        │     · Se activa desde el buscador cuando no hay coincidencias
        │     · Al guardar, aterriza directo en la Ficha del Paciente recién creado
        │
        └── ADMINISTRACIÓN (Django admin, sin tocar — acceso solo para rol Administrador,
              enlace discreto en el menú de usuario, no en la navegación principal)
```

**Decisión clave:** no hay "sección de consentimientos" ni "sección de historia clínica" como pantallas independientes. Todo vive **dentro** de la Ficha del Paciente, en paneles/pestañas de la misma vista, para cumplir tu punto 2 (todo desde una única pantalla).

---

## 2. Flujo del usuario (paso a paso, con conteo de clics)

### Paciente nuevo, primer consentimiento
```
1. Escribir en buscador (documento o nombre)         [0 clics, solo tecleo]
2. "No se encontró — Crear paciente"                 [1 clic]
3. Formulario corto (nombre, documento, tel., ¿menor?) [llenar + 1 clic "Guardar"]
   → aterriza automáticamente en Ficha del Paciente
4. Botón "Nuevo consentimiento" en la Ficha           [1 clic]
5. Panel lateral: elegir tipo (2 opciones grandes)    [1 clic]
6. Revisar texto + casilla de autorización            [1 clic "Continuar"]
7. Firmar en pantalla (canvas)                        [firma + 1 clic "Confirmar"]
   → PDF se genera solo, queda listado en la Ficha
```
**Total: ~5 clics + 2 formularios cortos.** (vs. ~15 clics actuales cruzando el admin dos veces).

### Paciente existente, consulta rápida
```
1. Escribir en buscador                               [0 clics]
2. Clic en el resultado                                [1 clic]
   → Ficha del Paciente con todo visible: historia, consentimientos previos, botón nuevo
```
**Total: 1 clic.**

---

## 3. Wireframes conceptuales (texto/ASCII — sin código todavía)

### 3.1 Panel (inicio)
```
┌──────────────────────────────────────────────────────────┐
│ 🦷 Clínica R                    [ Buscar paciente...  🔍] │
├──────────────────────────────────────────────────────────┤
│                                                            │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│   │ Pendientes │  │ Firmados   │  │ Este mes   │          │
│   │    7       │  │  hoy: 3    │  │    41      │          │
│   └────────────┘  └────────────┘  └────────────┘          │
│                                                            │
│   Pacientes recientes                                      │
│   ┌──────────────────────────────────────────────┐        │
│   │ 🙂 Valeria Upegui   CC 1035000842   Pendiente │        │
│   │ 🙂 Juan Pérez        CC 1098765432   Firmado  │        │
│   └──────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
```

### 3.2 Ficha del Paciente (pantalla central — todo en un solo scroll, sin pestañas ocultas)
```
┌──────────────────────────────────────────────────────────┐
│ ← Volver          Valeria Upegui Camacho · CC 1035000842   │
│                                          [ Editar datos ] │
├──────────────────────────────────────────────────────────┤
│ RESUMEN                        │ ACCIONES RÁPIDAS         │
│ Edad: 16 · Menor: Sí            │ [+ Nuevo consentimiento] │
│ Acudiente: María Camacho        │ [  Ver historia clínica] │
│ Tel: 300 000 0000               │                          │
├──────────────────────────────────────────────────────────┤
│ CONSENTIMIENTOS                                            │
│ ┌────────────────────────────────────────────────────┐    │
│ │ Ortodoncia Interceptiva   Firmado  15/07/2026  [PDF]│    │
│ │ Ortodoncia General        Pendiente            [Firmar]│  │
│ └────────────────────────────────────────────────────┘    │
├──────────────────────────────────────────────────────────┤
│ HISTORIA CLÍNICA (resumen expandible, no nueva pantalla)   │
│ Motivo de consulta: ...                                    │
│ Últimas evoluciones: ...                                   │
└──────────────────────────────────────────────────────────┘
```

### 3.3 Panel lateral de firma (se abre sobre la Ficha, no navega a otra URL)
```
                                    ┌────────────────────────┐
                                    │ Firmar consentimiento × │
                                    │ Ortodoncia General      │
                                    ├────────────────────────┤
                                    │ [texto legal scrollable]│
                                    │                          │
                                    │ ☐ Autorizo uso expediente│
                                    │                          │
                                    │  Firma del paciente:     │
                                    │  ┌────────────────────┐  │
                                    │  │   (canvas táctil)   │  │
                                    │  └────────────────────┘  │
                                    │  [Limpiar] [Confirmar]   │
                                    └────────────────────────┘
```

Este panel lateral (no una página nueva) es la pieza central del rediseño de flujo: cumple tu punto 2 literalmente — "todo desde una única pantalla".

---

## 4. Sistema de diseño (design tokens — la base de todo lo visual)

### 4.1 Paleta (del manual de marca, valores a confirmar contigo con el código hex exacto del archivo fuente si lo tienes en Figma/Illustrator; estos son los extraídos visualmente del PDF)

| Token | Valor aprox. | Uso |
|---|---|---|
| `--color-primario` | `#26453F` (verde inglés oscuro) | Fondos de marca, barra superior, texto de énfasis |
| `--color-secundario` | `#4C5F45` (verde oliva) | Estados hover, iconografía secundaria |
| `--color-terciario-1` | `#BFD4C6` (menta pálido) | Fondos suaves de tarjetas |
| `--color-terciario-2` | `#A9C877` (verde lima) | Acentos, badges positivos ("Firmado") |
| `--color-complementario` | `#F5EFDD` (crema) | Fondo general de la app |
| `--color-alerta` | `#C0392B` | Errores, campos obligatorios faltantes |
| `--color-pendiente` | `#D68910` | Badge "Pendiente" |
| `--color-texto` | `#1C2B27` | Texto principal sobre fondos claros |

### 4.2 Tipografía
- Títulos/UI: fallback web de "Microsoft Sans Serif" → `system-ui, "Segoe UI", sans-serif` (o `Inter` si prefieres una alternativa con más peso visual — a decidir contigo)
- Cuerpo/párrafos: fallback de "Avenir Light" → `"Nunito Sans", "Work Sans", sans-serif`
- Escala: `12/14/16/20/28/36px` para caption/body/subtítulo/título/héroe

### 4.3 Espaciado
Escala de 8px: `4, 8, 16, 24, 32, 48, 64px`. Elimina el actual `padding:20px;padding:36px` ad-hoc disperso en cada template (evidencia: `templates/base/panel.html` usa valores sueltos como `padding:36px` en línea, sin sistema).

### 4.4 Componentes del sistema (inventario completo, todos reutilizables)

| Componente | Reemplaza a | Notas |
|---|---|---|
| `Botón` (primario/secundario/peligro) | Botones inline con estilos repetidos (`.btn.n`, `.btn.o`, `.btn.sm` en CSS disperso) | Estados: normal/hover/disabled/loading |
| `Tarjeta` | Filas de tabla planas | Sombra suave, radio de borde consistente |
| `Badge de estado` | Texto plano con emoji (`&#9203; Pendiente`) | Componente visual con color semántico consistente |
| `Buscador con autocompletado` | Formulario GET simple con recarga | Resultados en vivo vía fetch, sin recargar página |
| `Panel lateral (drawer)` | Nueva URL completa por acción | Firmar y crear consentimiento ocurren sin abandonar la Ficha |
| `Modal de confirmación` | `messages.error/success` de Django solamente | Confirmaciones críticas (ej. "¿confirmar firma?") con modal, no solo banner |
| `Alerta/Toast` | `django.contrib.messages` renderizado como texto plano | Mismo mecanismo backend, presentación visual nueva (toast temporal, iconografía por tipo) |
| `Tabla de datos` | Tablas HTML básicas sin jerarquía visual | Encabezados sticky, filas con hover, orden visual claro |
| `Formulario` | Inputs sueltos sin agrupación | Agrupación por secciones, validación inline, campos obligatorios marcados consistentemente |
| `Stepper` (nuevo) | No existe | Para el asistente de consentimiento (elegir tipo → revisar → firmar) |
| `Firma táctil` | `<canvas>` actual, sin cambios de lógica | Solo contenedor visual nuevo alrededor del mismo mecanismo JS existente |

### 4.5 Iconografía
Set de iconos lineales consistente (una sola librería SVG, ligera, sin dependencias de build) para: paciente, consentimiento, firma, PDF, historia clínica, alerta, confirmación, editar, buscar. Actualmente el sistema usa emojis Unicode sueltos (`&#128203;`, `&#9203;`) — se reemplazan por iconografía de marca coherente.

---

## 5. Arquitectura del frontend

**Se mantiene la decisión técnica ya usada en el proyecto:** HTML + CSS + JS mínimo servido por Django templates, sin introducir un framework de build (React/Vue) — evita romper el despliegue actual en Railway y no añade complejidad de compilación a un proyecto que hoy no la tiene. El "sistema de diseño" se logra con:

```
static/
  css/
    tokens.css          ← variables de color/tipografía/espaciado (§4.1-4.3)
    components.css       ← botones, tarjetas, badges, modales, tablas (§4.4)
    layout.css            ← barra superior, grillas, paneles laterales
  js/
    buscador.js           ← autocompletado vía fetch a endpoint JSON
    drawer.js              ← apertura/cierre de paneles laterales sin recarga
    firma.js (existente)   ← se reutiliza tal cual, solo se re-empaqueta

templates/
  base/
    base.html              ← layout raíz con barra superior + tokens cargados
    _drawer.html            ← partial reutilizable para paneles laterales
    _toast.html             ← partial para mensajes
  pacientes/
    ficha.html               ← pantalla central (reemplaza detalle.html + lista.html separados)
    _crear_paciente.html     ← partial cargado dentro de un drawer
  consentimientos/
    _asistente.html           ← partial del stepper (elegir → revisar → firmar), cargado en drawer
```

**Principio de organización:** cada "acción" (crear paciente, nuevo consentimiento, firmar) es un **partial** que se inyecta en un drawer genérico, no una página nueva con su propia URL de navegación completa — así se logra el "todo en una pantalla" sin duplicar lógica de layout.

---

## 6. Jerarquía visual y principios de layout

1. **Un solo punto de entrada por tarea** — el buscador siempre visible en la barra superior es el único "menú" real del sistema.
2. **La Ficha del Paciente nunca compite por atención** — cuando está abierta, ocupa el 100% del área útil; los drawers se superponen sin navegar fuera.
3. **Máximo 2 niveles de profundidad** — Panel → Ficha del Paciente → Drawer de acción. Nunca 3 clics para llegar a hacer algo.
4. **Color con significado, no decorativo** — verde primario = estructura de marca; verde lima = éxito/firmado; ocre = pendiente; rojo = error. Nunca color sin función.
5. **Texto legal nunca se disfraza** — el consentimiento se muestra completo, con tipografía de cuerpo legible, dentro de un contenedor con scroll propio, nunca recortado ni minimizado por diseño.

---

## 7. Qué NO cambia (garantía de estabilidad — tu punto 9)

- Modelos, migraciones, esquema de base de datos: **sin cambios**.
- `services/pdf.py` (ReportLab), `services/drive.py`, `services/notificaciones.py`: **sin cambios de lógica**, solo se llaman desde las nuevas vistas igual que antes.
- Autenticación, roles (`LoginRequiredMiddleware`, `RoleContextMiddleware`): **sin cambios**.
- El `<canvas>` de firma y su JS de captura: **se reutiliza intacto**, solo cambia el contenedor visual alrededor.
- Panel de administración Django: **sigue existiendo**, accesible para el rol Administrador, sin alterar su funcionamiento.
- Todas las URLs actuales que ya funcionan (`/pacientes/<pk>/`, `/consentimientos/firmar/<pk>/`, etc.) **se conservan** — las nuevas se añaden encima, ninguna se elimina hasta confirmar que el nuevo flujo la reemplaza sin pérdida.

## 8. Consentimientos — trazabilidad sin migración de datos (tu punto 3, ajustado)

No se ejecuta ninguna migración de datos por adelantado. En su lugar:

1. Las plantillas nuevas (Ortodoncia General, Ortodoncia Interceptiva) se crean como **filas nuevas** en `PlantillaConsentimiento` durante la implementación (Fase de Módulo de Consentimientos, §9), con el texto legal completo de tus dos `.docx`, verbatim.
2. Las plantillas actuales se marcan `activa=False` **una por una, verificando primero que ningún flujo activo dependa de ellas** — no es un script masivo, es una acción puntual y reversible por plantilla.
3. Los consentimientos **ya firmados no se tocan en absoluto** — siguen apuntando a su plantilla original vía `ForeignKey`, con su texto ya congelado en `texto_generado` (campo que ya existe en el modelo, guarda una copia inmutable del texto al momento de la firma — confirmado en `consentimientos/models.py:60`). Esto significa que, técnicamente, **ya hay trazabilidad legal garantizada por diseño del sistema actual**, sin que se requiera ninguna acción adicional de mi parte para protegerla.

---

## 9. Estrategia de implementación (módulos, no fases genéricas)

Cada módulo se implementa, se verifica en local y Railway, y se documenta en `CHANGELOG_AUDITORIA.md` antes de continuar al siguiente.

1. **Módulo 0 — Blindaje:** corregir el bug latente (`requiere_autorización_expediente`), ya identificado, aislado de todo lo demás.
2. **Módulo 1 — Sistema de diseño base:** `tokens.css`, `components.css`, aplicado primero solo a `login.html` para validación visual contigo antes de expandir.
3. **Módulo 2 — Capa de navegación:** barra superior + buscador con autocompletado (backend JSON nuevo, sin tocar vistas existentes).
4. **Módulo 3 — Ficha del Paciente:** pantalla central unificada (historia + consentimientos + acciones), reemplaza `detalle.html` actual.
5. **Módulo 4 — Drawer de creación de paciente:** formulario corto, sin pasar por admin.
6. **Módulo 5 — Drawer/Stepper de consentimiento:** elegir tipo → revisar → firmar, reutilizando el canvas de firma existente.
7. **Módulo 6 — Plantillas nuevas de consentimiento:** carga de las 2 plantillas nuevas, desactivación puntual de las antiguas.
8. **Módulo 7 — Pulido visual integral:** modales, toasts, iconografía, estados de carga, mensajes de error específicos.
9. **Módulo 8 — Verificación final:** checklist completo (login, buscar, crear paciente, firmar ambos tipos de consentimiento nuevo, PDF, historia clínica, admin, roles) en local y Railway.

---

## 10. Lo que necesito de ti para arrancar

1. Confirmar los **hex exactos** de la paleta si los tienes en el archivo fuente de diseño (Figma/Illustrator), o autorizo a usar los valores extraídos visualmente del PDF (§4.1).
2. Decidir la tipografía web: ¿fallback de sistema (Segoe UI/Nunito Sans, gratis, sin licencia que gestionar) o prefieres que investigue una fuente con licencia web similar a Microsoft Sans Serif/Avenir?
3. Aprobación de este documento para iniciar por el Módulo 0.

No se modifica nada hasta tu aprobación.
