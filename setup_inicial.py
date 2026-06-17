"""
Configuración inicial del sistema.
Ejecutar UNA sola vez después de migrar.
"""
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
import django; django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import PerfilUsuario
from consentimientos.models import PlantillaConsentimiento

# ── Superusuario ────────────────────────────────────────────────────────────
admin, created = User.objects.get_or_create(username='admin')
if created:
    admin.set_password('SamuelRoldan2026!')
    admin.is_staff = True; admin.is_superuser = True
    admin.first_name = 'Administrador'; admin.last_name = 'Sistema'
    admin.save()
    PerfilUsuario.objects.create(usuario=admin, rol='ADMIN')
    print('✅ Superusuario admin creado.')

# ── Roles ───────────────────────────────────────────────────────────────────
apps_clinicas = ['pacientes', 'consentimientos', 'historial']
perms_todos = Permission.objects.filter(content_type__app_label__in=apps_clinicas)

rol_od, _ = Group.objects.get_or_create(name='Odontólogo')
rol_od.permissions.set(perms_todos.filter(codename__in=[
    'view_paciente', 'add_paciente', 'change_paciente',
    'view_consentimiento', 'add_consentimiento', 'change_consentimiento',
    'view_plantillaconsentimiento',
    'view_fichaClinica', 'add_fichaClinica', 'change_fichaClinica',
    'view_evolucionclinica', 'add_evolucionclinica', 'change_evolucionclinica',
    'view_odontograma', 'add_odontograma',
]))

rol_aux, _ = Group.objects.get_or_create(name='Auxiliar')
rol_aux.permissions.set(perms_todos.filter(codename__in=[
    'view_paciente', 'add_paciente', 'change_paciente',
    'view_consentimiento', 'add_consentimiento',
    'view_plantillaconsentimiento',
]))

print('✅ Roles Odontólogo y Auxiliar configurados.')

# ── Plantillas de consentimiento ─────────────────────────────────────────────
plantillas = [
    {
        'nombre': 'Consentimiento Informado — Ortodoncia',
        'tipo': 'ORTODONCIA',
        'texto': """Se me ha explicado verbalmente toda la información específica relacionada con el tratamiento odontológico que me ha sido recomendado. La información hace referencia a los siguientes temas: justificación científica de la realización del (los) procedimiento(s) que me ha(n) sido recomendado(s), preparación y condiciones previas del paciente para hacer viable la realización del (los) tratamiento(s) como estar libre de caries y enfermedad de las encías y haber visitado recientemente al Odontólogo para la limpieza general previa, mantenimiento de mis visitas periódicas, explicación sobre la metodología o la forma como se realiza el(los) procedimiento(s) recomendado(s), así como el haberme mostrado físicamente los aditamentos con los que se hará el tratamiento, el tiempo aproximado de duración y las actividades que se realizan en las distintas citas; también las incomodidades que pueden producir dicho(s) procedimiento(s) como cierta sensibilidad de los dientes luego del cambio del alineador o la colocación o reposición de Brackets o auxiliares y las precauciones con la higiene oral. Información general sobre los riesgos y complicaciones previstas. Los posibles y más importantes beneficios del tratamiento, así como el plan de mi tratamiento me fue explicado con detalle y en términos que comprendí luego de la explicación que me hizo el profesional y su personal auxiliar.

Mediante la presente, yo como paciente y/o el representante confirmo que: se me han comunicado las principales consideraciones y los principales riesgos del tratamiento de Ortodoncia. He leído y entendido este documento y el anexo de diagnóstico, objetivos y plan de tratamiento y comprendo que además pueden existir otros problemas que ocurren con menos frecuencia o son menos severos.

Se me ha expuesto el tratamiento de Ortodoncia para solucionar mi anomalía y se me ha presentado información para ayudarme a tomar mi decisión, otorgándoseme la oportunidad de aclarar todos los cuestionamientos sobre el tratamiento propuesto y la información contenida en este documento. Por consiguiente, consiento a que se me proporcione el tratamiento de Ortodoncia. Declaro (declaramos) que autorizo (autorizamos) al Odontólogo y al personal auxiliar respectivo a realizar todos los procedimientos conexos y complementarios con la atención principal que se ofrece y que he (hemos) aceptado voluntariamente.

Se me ha informado el valor del tratamiento y he convenido su forma de pago. He firmado y conozco que debo cumplir las citas ortodóncicas asignadas y que, en caso de inasistencia por un período de tres meses sin justa causa, se podrá dar por terminado el contrato de prestación de servicios profesionales. Otra forma de terminación anticipada del tratamiento se deberá al no pago de los honorarios profesionales acordados, no dándose lugar a restitución. Así mismo, acepto pagar los cargos adicionales por pérdida de alineadores, Brackets o auxiliares, alineadores, Brackets o auxiliares rotos por mal uso o mal trato y los que no se adapten por su uso inconstante. Así mismo por la pérdida y/o rotura de los auxiliares usados para mi tratamiento como botones, brackets, resinas, miniimplantes u otros que se me coloquen o me indiquen usar.""",
        'requiere_autorizacion_expediente': True,
    },
    {
        'nombre': 'Consentimiento Informado — Exodoncia',
        'tipo': 'EXODONCIA',
        'texto': """Se me ha explicado el procedimiento de extracción dental (exodoncia) para el (los) diente(s) indicado(s) por el odontólogo. He sido informado sobre las razones por las cuales se recomienda esta extracción, los procedimientos alternativos disponibles, y los riesgos y complicaciones potenciales del procedimiento.

Entiendo que las complicaciones posibles incluyen, entre otras: infección, sangrado prolongado, daño a dientes o tejidos adyacentes, trismo (dificultad para abrir la boca), parestesia temporal o permanente, comunicación oroantral, y alveolitis (hueso seco).

He sido informado sobre los cuidados postoperatorios necesarios: no fumar, no escupir ni usar popote por 24 horas, aplicar frío local, tomar los medicamentos recetados y asistir a los controles programados.

Declaro que he tenido la oportunidad de hacer todas las preguntas que he considerado necesarias y que han sido respondidas a mi satisfacción. Acepto voluntariamente el procedimiento de extracción dental indicado.""",
        'requiere_autorizacion_expediente': True,
    },
    {
        'nombre': 'Consentimiento Informado — Endodoncia',
        'tipo': 'ENDODONCIA',
        'texto': """Se me ha explicado en qué consiste el tratamiento de conductos (endodoncia) para el diente indicado por el odontólogo. He sido informado que este procedimiento tiene como objetivo eliminar la pulpa dental infectada o inflamada para conservar el diente.

Entiendo que el procedimiento puede requerir varias sesiones y que, aunque se toman todas las precauciones necesarias, pueden presentarse complicaciones como: fractura de instrumentos dentro del conducto, perforación radicular, reacción a los materiales utilizados, fracaso del tratamiento que podría requerir cirugía apical o extracción del diente.

He sido informado que después del tratamiento el diente puede requerir una restauración definitiva como una corona para protegerlo adecuadamente.

Consiento voluntariamente a que se realice el tratamiento de endodoncia en el diente indicado, así como los procedimientos complementarios que se consideren necesarios durante el tratamiento.""",
        'requiere_autorizacion_expediente': True,
    },
]

for datos in plantillas:
    obj, created = PlantillaConsentimiento.objects.get_or_create(
        nombre=datos['nombre'], defaults={**datos, 'version': 1, 'activa': True, 'creado_por': admin})
    if created:
        print(f'✅ Plantilla creada: {datos["nombre"]}')

print('\n' + '='*50)
print('SISTEMA LISTO')
print('Usuario: admin | Clave: SamuelRoldan2026!')
print('IMPORTANTE: Cambiar la clave al primer ingreso.')
print('='*50)
