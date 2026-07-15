"""
Corrige ortografia en todos los templates del sistema.
Ejecutar en C:\\samuel_roldan:
  python fix_ortografia.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(BASE, 'templates')

# Mapa de correcciones: texto incorrecto -> texto correcto
CORRECCIONES = {
    # Login
    'Consultorio Odontologico Samuel Roldan': 'Consultorio Odontológico Samuel Roldán',
    'Sistema de Gestion de Consentimientos Informados': 'Sistema de Gestión de Consentimientos Informados',
    'CONTRASENA': 'CONTRASEÑA',
    'Contrasena': 'Contraseña',
    'contrasena': 'contraseña',
    'Iniciar sesion': 'Iniciar sesión',
    'Iniciar Sesion': 'Iniciar sesión',
    'Usuario o contrasena incorrectos': 'Usuario o contraseña incorrectos',

    # Navbar y panel
    'Samuel Roldan': 'Samuel Roldán',
    'ORTODONCISTA': 'Ortodoncista',
    'Odontologo': 'Odontólogo',
    'odontologo': 'odontólogo',
    'Odontologico': 'Odontológico',
    'Pendientes de firma': 'Pendientes de firma',
    'Firmados hoy': 'Firmados hoy',
    'Este mes': 'Este mes',
    'Pacientes activos': 'Pacientes activos',
    'Ver todos': 'Ver todos',
    'Crear el primero': 'Crear el primero',
    'Sin consentimientos aun': 'Sin consentimientos aún',
    'Buscar Paciente': 'Buscar paciente',
    'Nuevo Paciente': 'Nuevo paciente',
    'Firmar Consentimiento': 'Firmar consentimiento',
    'Salir &rarr;': 'Salir →',

    # Admin
    'Consultorio Odontologico Samuel Roldan': 'Consultorio Odontológico Samuel Roldán',
    'Sistema de Gestion': 'Sistema de Gestión',
    'Ortodoncista · Sistema de Gestion': 'Ortodoncista · Sistema de Gestión',

    # Pacientes
    'Sin pacientes registrados': 'Sin pacientes registrados',
    'Sin resultados para': 'Sin resultados para',
    'encontrado': 'encontrado',

    # Consentimientos
    'Consentimientos recientes': 'Consentimientos recientes',
    'Pendientes de firma': 'Pendientes de firma',
    'Nuevo consentimiento': 'Nuevo consentimiento',
    'Ver todos &rarr;': 'Ver todos →',

    # Footer
    'Consultorio Odontologico Samuel Roldan': 'Consultorio Odontológico Samuel Roldán',

    # Firmar
    'Firma del paciente': 'Firma del paciente',
    'Firma del acudiente': 'Firma del acudiente',
    'Confirmar y firmar': 'Confirmar y firmar',
    'Autorizacion': 'Autorización',
    'autorizacion': 'autorización',
    'informacion': 'información',
    'Informacion': 'Información',
    'procedimiento': 'procedimiento',
    'Procedimiento': 'Procedimiento',
    'educacion': 'educación',
    'investigacion': 'investigación',
    'publicacion': 'publicación',
    'SI autorizo': 'SÍ, autorizo',
    'NO autorizo': 'NO autorizo',
    'Firmado el': 'Firmado el',
    'Guardando...': 'Guardando...',
    'anos': 'años',
}

def corregir_archivo(ruta):
    with open(ruta, encoding='utf-8') as f:
        contenido = f.read()

    original = contenido
    for incorrecto, correcto in CORRECCIONES.items():
        contenido = contenido.replace(incorrecto, correcto)

    if contenido != original:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return True
    return False

print("\n=== CORRIGIENDO ORTOGRAFIA ===\n")
total = 0
for raiz, dirs, archivos in os.walk(TPL):
    for archivo in archivos:
        if archivo.endswith('.html'):
            ruta = os.path.join(raiz, archivo)
            if corregir_archivo(ruta):
                print(f'  OK -> {os.path.relpath(ruta, BASE)}')
                total += 1

print(f"\n{total} archivo(s) corregido(s)")
print("\nAhora ejecuta:")
print("  git add -A")
print("  git commit -m 'fix ortografia templates'")
print("  git push")
