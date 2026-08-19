"""
Comando de gestión: carga las nuevas plantillas de consentimiento de
Clínica R y desactiva las plantillas anteriores, UNA POR UNA, sin borrar
ninguna fila (los consentimientos ya firmados conservan su ForeignKey y su
texto_generado congelado — no se pierde trazabilidad legal).

Uso:
    python manage.py cargar_plantillas_clinica_r
    python manage.py cargar_plantillas_clinica_r --dry-run   (solo muestra qué haría)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from consentimientos.models import PlantillaConsentimiento

TEXTO_ORTODONCIA_GENERAL = """MI TRATAMIENTO

DE

ORTODONCIA con Alineadores, Brackets y auxiliares.

INFORMACIÓN PARA QUE EL PACIENTE/ACUDIENTE

OTORGUE SU CONSENTIMIENTO/ASENTIMIENTO.

La ORTODONCIA procura mejorar la oclusión ayudando a dirigir las fuerzas ejercidas sobre los dientes, para protegerlos del trauma durante las actividades de masticación, deglución de alimentos y del habla ente otras. También trata de distribuir la tensión de la masticación por toda la boca para minimizar la presión excesiva en los huesos, las raíces de los dientes, las encías, y las articulaciones temporomandibulares. Mediante el tratamiento ortodóncico se puede llegar a eliminar posibles problemas dentales, inclusive el desgaste anormal de los dientes.  La Ortodoncia puede también propiciar una sonrisa agradable y mejorar la imagen personal y la autoestima.

BENEFICIOS:

La Ortodoncia juega un importante papel en el mejoramiento de toda la salud Oral y en la obtención de la armonía entre los dientes y la cara para una sonrisa agradable y saludable.  Una sonrisa atractiva mejora la autoestima lo cual puede mejorar la calidad de vida por sí misma.  Los dientes bien alineados son más fáciles de limpiar, lo que puede reducir el riesgo de caries, enfermedades de las encías y del hueso de soporte.

Debido a las condiciones individuales actuales y a las limitaciones del tratamiento debidas a variabilidad propia de la naturaleza y del ser humano, la obtención de todos los objetivos puede no ser lograda en su totalidad.

CONDICIONES:

- Es posible que el tratamiento se demore más de lo previsto y que requiera un mayor tiempo al estimado inicialmente para completar el tratamiento. Un crecimiento excesivo o deficiente del hueso, la poca cooperación en el uso de los alineadores, Brackets o auxiliares como se recomienda, la higiene bucal insuficiente, la pérdida o daño de alineadores, Brackets o auxiliares y el no acudir regularmente a las consultas pueden demorar el tiempo del tratamiento y afectar la calidad de los resultados definidos inicialmente.  Esto requeriría una evaluación de las causas de la limitación del logro de los objetivos de la forma y el tiempo propuesto inicialmente y posiblemente revaluar los objetivos y condiciones de mi tratamiento.

- Para asegurar una eficacia clínica mínima en un tratamiento con alineadores, debo usarlos 22 horas por día en conjunto con los Brackets o auxiliares el tiempo que se me indique. No cumplir con las horas mínimas puede disminuir la predictibilidad de los resultados clínicos.

- Para aumentar la predictibilidad del tratamiento se requiere la cementación de ABCs (Aditamentos Biomecánicos Complementarios) a uno o más dientes, como resinas en forma de topes, botones, brackets, brazos metálicos y elásticos fijos o removibles, entre otros.  Estos se pueden caer y requerir sustitución y serán removidos al finalizar el tratamiento.* *

- En algunos casos se puede requerir técnicas dentales de rehabilitación o de otro tipo, las cuales son incorporadas en el plan de tratamiento.  Estos tratamientos se denominan “Interdisciplinarios”, es decir, que debe participar tanto en la planeación como en la ejecución otro u otros profesionales. Esto se requiere en ocasiones en los que los objetivos no sean alcanzables solo con el uso de alineadores o que se identifiquen limitaciones que tanto antes como durante el tratamiento deban ser evaluadas o tratadas por otros profesionales.

- Además de las revisiones o tratamientos que otros profesionales deben llevar a cabo, es indispensable mantener las revisiones y tratamientos que el odontólogo general o quien yo tenga como “Mi Odontólogo”, realice.

- En algunos casos en los que se deba conseguir espacio para el logro de los objetivos, podría estar indicado que deba hacerme extracciones dentales o desgaste interproximal de algunos dientes lo cual me ha sido explicado tanto en su justificación como en el procedimiento, los beneficios y los riesgos que conlleva.

- Los alineadores no deben deteriorarse con un uso adecuado, el cual se me explicó con detalle. En caso de su rotura o la de los Brackets o auxiliares entiendo que debo asumir los costos de las reposiciones y entiendo que esto puede limitar el logro de los objetivos propuestos o retrasarlos.

- En algunos casos, al final del tratamiento puede ser necesario realizar un “ajuste oclusal” para eliminar contactos oclusales fuertes.

- Es normal en todos los pacientes una tendencia permanente al cambio de posiciones de los dientes después del tratamiento. Una vez terminado el tratamiento, continúa una etapa llamada “PROGRAMA DE RETENCIÓN”. En esta se tienen citas periódicas de supervisión durante los doce (12) meses siguientes para controlar y minimizar los posibles cambios en la oclusión y posiciones de los dientes que ocurren cuando se retira la aparatología ortodóncica.  En esta etapa es indispensable el uso de aditamentos diferentes o retenedores de manera constante y permanente.  Luego de este período y de manera individual, se disminuye su uso, pero no se suspende, para poder mantener en el largo plazo el resultado obtenido al finalizar el tratamiento.  Pacientes que no usan los retenedores prescritos por el ortodoncista tendrán más posibilidades de recidiva [volver a tener] la anomalía tratada o presentar cambios en las posiciones dentales y la oclusión por efectos del proceso de maduración y envejecimiento natural, el cual es variable e individual.  Luego del primer año de supervisión debo continuar mis revisiones con el Odontólogo general de acuerdo con las recomendaciones mi Ortodoncista.

- En algunos casos, para efectos del logro del resultado ideal (por ejemplo, el cierre total del espacio excesivo) se requiere tratamiento dental restaurativo debido a la gran variación de tamaño y forma de los dientes. Los tipos más comunes de tratamiento son la consolidación cosmética, el tratamiento restaurativo de coronas y puentes y /o terapia periodontal (De los tejidos de soporte de los dientes).

- Afectación del tratamiento por problemas médico-odontológicos generales. Entiendo que debo mantener informado al Ortodoncista sobre cualquier cambio en mi salud general u oral.

RIESGOS:

Los principales riesgos que asumo con el tratamiento de Ortodoncia pueden incluir:

- Aunque es poco frecuente, existe la probabilidad de ruptura del alineador o los Brackets o auxiliares, con la consecuente posibilidad de aspirar o ingerir partes.

- Aunque es poco frecuente, existe la posibilidad de aparición de reacciones alérgicas al material del alineador.

- Caries, enfermedades de las encías y marcas permanentes, descalcificación de la dentadura, los cuales son causados por la realización incompleta e inadecuada de la higiene oral, sobre la cual fui ampliamente instruido.

- Sensibilidad en los dientes después de cambiar al siguiente alineador o la activación de los Brackets o auxiliares.

- Afectación transitoria del habla, produciendo un “seseo” que regularmente se resuelve en un periodo corto de tiempo.

- Aumento temporal de la saliva o sequedad de boca.

- Molestias debido a cambios en la mordida durante el tratamiento.

- Reducción de la longitud de las raíces de las piezas dentarias, lo que a la postre puede constituir una amenaza para dichas piezas.

- Problemas en la retención (que se afloje con facilidad) del alineador e impedimento en el movimiento dental debido a que las coronas de los dientes sean cortas (dientes pequeños).

- Inflamación de las encías y posible pérdida del hueso alveolar, especialmente cuando el paciente no remueve diariamente la placa bacteriana con una buena higiene bucal.

- Un diente que previamente haya sido golpeado o sometido a procedimientos de rehabilitación puede manifestar cambios imprevisibles. En ciertos casos, la vida útil del diente puede disminuir, pudiendo requerir tratamientos dentales complementarios tales como Endodoncia y/o restauración adicional, y/o la pérdida de la pieza dental.

- Afectación y/o cambio de mis restauraciones dentales existentes que pueden requerir una nueva cementación o su reemplazo.

- Disminución del tejido de soporte en los dientes que han sido movidos. En estos casos, después de alinear los dientes, pueden aparecer espacios en forma de triángulo que en condiciones normales debería estar ocupado por la encía y que usualmente es posible mejorar con el tratamiento de Ortodoncia, pero que en ocasiones permanecen y que pueden ser mejorados por técnicas de manejo de las encías por parte del Odontólogo general o de un especialista.

- Daños o deterioros en el nervio de una pieza dental.

- Lesiones en las piezas dentales o en la boca, por accidentes ocurridos con la manipulación de instrumentos dentales.

- Disminución de la posibilidad de lograr el resultado buscado con el tratamiento, por la formación atípica de los dientes o los cambios insuficientes en el desarrollo de los maxilares.

ALTERNATIVAS POSIBLES

Para la gran mayoría de los pacientes, el tratamiento de Ortodoncia es un procedimiento electivo.  Las diferentes alternativas para mi tratamiento me han sido explicadas, incluso la posibilidad de no realizarlo.  Con la decisión de no hacerlo acepto mi condición actual y decido vivir sin la corrección o mejoría ortodóncica.  Las posibles alternativas para mi tratamiento me han sido explicadas con sus respectivos beneficios, riesgos y limitaciones.

CONSTANCIA DE LA INFORMACIÓN QUE LE HA SIDO SUMINISTRADA Y EXPLICADA AL PACIENTE Y AL ACUDIENTE DE SUS DECISIONES SOBRE LA ACEPTACIÓN O NO DEL (LOS) PROCEDIMIENTO(S) QUE LE HA(N) SIDO RECOMENDADOS Y OTROS ASUNTOS CONEXOS.

Se me ha explicado verbalmente toda la información específica relacionada con el tratamiento ortodóncico que me ha sido recomendado.  La información hace referencia básicamente a los siguientes temas: Justificación científica de la realización del (los) procedimiento(s) que me ha(n) sido recomendado(s), preparación y condiciones previas del paciente para hacer viable la realización del (los) tratamiento(s) como estar libre de caries y enfermedad de las encías y haber visitado recientemente al Odontólogo para la limpieza general previa, mantenimiento de mis visitas periódicas a “Mi Odontólogo”; explicación sobre la metodología o la forma como se realiza el(los) procedimiento(s) recomendado(s), así como el haberme mostrado físicamente los aditamentos con los que se hará el tratamiento, el tiempo aproximado de duración y las actividades que se realizan en las distintas citas;  también las incomodidades que puede(n) producir dicho(s) procedimiento(s) como cierta sensibilidad de los dientes luego del cambio del alineador o la colocación o reposición de Brackets o auxiliares y las precauciones con la higiene oral.  Información general sobre los riesgos y complicaciones previstas. Los posibles y más importantes beneficios del tratamiento, así como el plan de mi tratamiento me fue explicado con detalle y en términos que comprendí luego de la explicación que me hizo el profesional y su personal auxiliar.

Mediante la presente, yo como paciente y/o el representante confirma que: se me han comunicado las principales consideraciones y los principales riesgos del tratamiento de Ortodoncia.  He leído y entendido este documento y el anexo de diagnóstico, objetivos y plan de tratamiento y comprendo que además pueden existir otros problemas que ocurren con menos frecuencia o son menos severos.

Se me ha expuesto el tratamiento de Ortodoncia para solucionar mi anomalía y se me ha presentado información para ayudarme a tomar mi decisión, otorgándoseme la oportunidad de aclarar todos los cuestionamientos sobre el tratamiento propuesto y la información contenida en este documento.  Por consiguiente, consiento a que se me proporcione el tratamiento de Ortodoncia. Declaro (declaramos) que autorizo (autorizamos) al Odontólogo y al personal auxiliar respectivo a realizar todos los procedimientos conexos y complementarios con la atención principal que se ofrece y que he (hemos) aceptado voluntariamente.

Se me ha informado el valor del tratamiento y he convenido su forma de pago.  He firmado y conozco que debo cumplir las citas ortodóncicas asignadas y que, en caso de inasistencia por un período de tres meses sin justa causa, se podrá dar por terminado el contrato de prestación de servicios profesionales.  Otra forma de terminación anticipada del tratamiento se deberá al no pago de los honorarios profesionales acordados, no dándose lugar a restitución.  Así mismo, acepto pagar los cargos adicionales por pérdida de alineadores, Brackets o auxiliares, alineadores, Brackets o auxiliares rotos por mal uso o mal trato y los que no adapten por su uso inconstante. Así mismo por la perdida y/o rotura de los auxiliares usados para mi tratamiento como botones, brackets, resinas, minimplantes u otros que se me coloquen o me indiquen usar.

Igualmente, SI (  ) NO (  ) autorizo el uso del expediente con sus registros y exámenes de Ortodoncia con fines de consultas profesionales, investigación, educación o publicación en revistas profesionales."""

TEXTO_ORTODONCIA_INTERCEPTIVA = """MI TRATAMIENTO

DE

ORTODONCIA INTERCEPTIVA

INFORMACIÓN PARA QUE EL ACUDIENTE

OTORGUE SU CONSENTIMIENTO Y EL ACUDIENTE SU ASENTIMIENTO.

La ORTODONCIA INTERCEPTIVA procura mejorar la oclusión ayudando a dirigir las fuerzas ejercidas sobre los dientes, para protegerlos del trauma durante las actividades de masticación, deglución de alimentos y del habla ente otras .  También trata de distribuir la tensión de la masticación por toda la boca para minimizar la presión excesiva en los huesos, las raíces de los dientes, las encías, y las articulaciones temporomandibulares. Mediante el tratamiento ortodóncico se puede llegar a eliminar posibles problemas dentales, inclusive el desgaste anormal de los dientes.  La Ortodoncia puede también propiciar una sonrisa agradable y mejorar la imagen personal y la autoestima.

BENEFICIOS:

La Ortodoncia juega un importante papel  en el mejoramiento de toda la salud Oral y en la obtención de la armonía entre los dientes y la cara para una sonrisa agradable y saludable.  Una sonrisa atractiva mejora la autoestima lo cual puede mejorar la calidad de vida por si misma.  Los dientes bien alineados son más fáciles de limpiar, lo que puede reducir el riesgo de caries, enfermedades de las encías y del hueso de soporte.

Debido a las condiciones individuales actuales y a las limitaciones del tratamiento debidas a variabilidad propia de la naturaleza y del ser humano, la obtención de todos los objetivos puede no ser lograda en su totalidad.

CONDICIONES:

- Es posible que el tratamiento se demore mas de lo previsto y que requiera un mayor tiempo al estimado inicialmente para completar el tratamiento. Un crecimiento excesivo o deficiente del hueso, la poca cooperación en el uso y/o manejo de los aparatos como se recomienda, la higiene bucal insuficiente, la pérdida o daño de estos y el no acudir regularmente a las consultas pueden demorar el tiempo del tratamiento y afectar la calidad de los resultados definidos inicialmente.  Esto requeriría una evaluación de las causas de la limitación del logro de los objetivos de la forma y el tiempo propuesto inicialmente y posiblemente revaluar los objetivos y condiciones de mi tratamiento.

- Para asegurar una eficacia clínica mínima en un tratamiento con aparatos removibles, debo usarlos 22 horas por día como mínimo a menos que se indique lo contrario, en conjunto con los Brackets o auxiliares el tiempo que se me indique. No cumplir con las horas mínimas puede disminuir la predecibilidad de los resultados clínicos.

- Para aumentar la predecibilidad del tratamiento se requiere la cementación de algunos auxiliares a uno o más dientes, como resinas en forma de topes, botones, brackets, brazos metálicos y elásticos fijos o removibles, entre otros.  Estos se pueden caer y requerir sustitución y serán removidos al finalizar el tratamiento.* *

- En algunos casos se puede requerir técnicas dentales de rehabilitación o de otro tipo, las cuales son incorporadas en el plan de tratamiento.  Estos tratamientos se denominan “Interdisciplinarios”, es decir, que debe participar tanto en la planeación como en la ejecución otro u otros profesionales. Esto se requiere en ocasiones en los que los objetivos no sean alcanzables solo con el uso de alineadores o que se identifiquen limitaciones que tanto antes como durante el tratamiento deban ser evaluadas o tratadas por otros profesionales.

- Además de las revisiones o tratamientos que otros profesionales deben llevar a cabo, es indispensable mantener las revisiones y tratamientos que el odontólogo general o quien yo tenga como “Mi Odontólogo”, realice.

- En algunos casos en los que se deba conseguir espacio para el logro de los objetivos, podría estar indicado que deba hacerme extracciones dentales o  desgaste interproximal de algunos dientes, lo cual me ha sido explicado tanto en su justificación como en el procedimiento, los beneficios y los riesgos que conlleva.

- Los aparatos no deben deteriorarse con un uso adecuado el cual se me explicó con detalle. En caso de su rotura o la de los Brackets o auxiliares, entiendo que debo asumir los costos de las reposiciones y entiendo que esto puede limitar el logro de los objetivos propuestos o retrasarlos.

- En algunos casos, al final del tratamiento puede ser necesario realizar un “ajuste oclusal” para eliminar contactos oclusales fuertes.

- Es normal en todos los pacientes una tendencia permanente al cambio de posiciones de los dientes después del tratamiento. Una vez terminado el tratamiento, continúa una etapa llamada “PROGRAMA DE RETENCIÓN”. En esta se tienen citas periódicas de supervisión durante los doce (12) meses siguientes para controlar y minimizar los posibles cambios en la oclusión y posiciones de los dientes que ocurren cuando se retiran los aparatos.  En esta etapa es indispensable el uso de aditamentos diferentes o retenedores de manera constante y permanente.  Luego de este período y de manera individual, se disminuye su uso pero no se suspende, para poder mantener en el largo plazo el resultado obtenido al finalizar el tratamiento.  Pacientes que no usan los retenedores prescritos por el ortodoncista tendrán más posibilidades de recidiva [volver a tener] la anomalía tratada o presentar cambios en las posiciones dentales y la oclusión por efectos del proceso de maduración y envejecimiento natural, el cual es variable e individual.  Luego del primer año de supervisión debo continuar mis revisiones con el Odontologo general de acuerdo con las recomendaciones de mi Ortodoncista.

- En algunos casos, para efectos del logro del resultado ideal (por ejemplo, el cierre total del espacio excesivo) se requiere tratamiento dental restaurativo debido a la gran variación de tamaño y forma de los dientes. Los tipos más comunes de tratamiento son la consolidación cosmética, el tratamiento restaurativo de coronas y puentes y /o terapia periodontal (De los tejidos de soporte de los dientes).

- Afectación del tratamiento por problemas médico-odontológicos generales. Entiendo que debo mantener informado al Ortodoncista sobre cualquier cambio en mi salud general u oral.

- Luego de realizado el tratamiento de Ortodoncia Interceptiva es probable que algunos dientes erupcionen en mala posición, que el crecimiento craneofacial sea inadecuado o que la mordida no se consolide de manera adecuada.  Por tanto, luego de terminar el recambio dental se debe hacer una evaluación para establecer la necesidad de realizar un tratamiento de Ortodoncia correctiva.

RIESGOS:

Los principales riesgos que asumo con el tratamiento de Ortodoncia pueden incluir:

- Aunque es poco frecuente, existe la probabilidad de ruptura de los aparatos removibles o fijos o los Brackets o auxiliares con la consecuente posibilidad de aspirar o ingerir partes.

- Aunque es poco frecuente, existe la posibilidad de aparición de reacciones alérgicas al material del alineador.

- Caries, enfermedades de las encías y marcas permanentes, descalcificación de la dentadura, los cuales son causados por la realización incompleta e inadecuada de la higiene oral, sobre la cual fui ampliamente instruido.

- Sensibilidad en los dientes después de cambiar o activar los aparatos o la activación de los Brackets o auxiliares.

- Afectación transitoria del habla, produciendo un “seseo” que regularmente se resuelve en un periodo corto de tiempo

- Aumento temporal de la saliva como sequedad de boca.

- Molestias debido a cambios en la mordida durante el tratamiento.

- Reducción de la longitud de las raíces de las piezas dentarias, lo que a la postre puede constituir una amenaza para dichas piezas.

- Problemas en la retención (que se afloje con facilidad) de los aparatos e impedimento en el movimiento dental debido a que las coronas de los dientes sean cortas (dientes pequeños).

- Inflamación de las encías y posible pérdida del hueso alveolar, especialmente cuando el paciente no remueve diariamente la placa bacteriana con una buena higiene bucal.

- Un diente que previamente haya sido golpeado o sometido a procedimientos de rehabilitación puede manifestar cambios imprevisibles. En ciertos casos, la vida útil del diente puede disminuir,  pudiendo requerir tratamientos dentales complementarios tales como Endodoncia y/o restauración adicional, y/o la pérdida de la pieza dental.

- Afectación y/o cambio de mis restauraciones dentales existentes que pueden requerir una nueva cementación o su reemplazo.

- Disminución del tejido de soporte en los dientes que han sido movidos. En estos casos, después de alinear los dientes, pueden aparecer espacios en forma de triangulo que en condiciones normales debería estar ocupado por la encía y que usualmente es posible mejorar con el tratamiento de Ortodoncia, pero que en ocasiones permanecen y que pueden ser mejorados por técnicas de manejo de las encías por parte del Odontólogo general o de un especialista.

- Daños o deterioros en el nervio de una pieza dental.

- Lesiones en las piezas dentales o en la boca, por accidentes ocurridos con la manipulación de instrumentos dentales.

- Disminución de la posibilidad de lograr el resultado buscado con el tratamiento, por la formación atípica de los dientes o los cambios insuficientes en el desarrollo de los maxilares.

ALTERNATIVAS POSIBLES

Para la gran mayoría de los pacientes, el tratamiento de Ortodoncia es un procedimiento electivo.  Las diferentes alternativas para mi tratamiento me han sido explicadas, incluso la posibilidad de no realizarlo.  Con la decisión de no hacerlo acepto mi condición actual y decido vivir sin la corrección o mejoría ortodóncica.  Las posibles alternativas para mi tratamiento me han sido explicadas con sus respectivos beneficios, riesgos y limitaciones.

CONSTANCIA DE LA INFORMACIÓN QUE LE HA SIDO SUMINISTRADA Y  EXPLICADA AL PACIENTE Y SU ACUDIENTE Y DE SUS DECISIONES SOBRE LA ACEPTACIÓN O NO DEL (LOS) PROCEDIMIENTO(S) QUE LE(S) HA(N) SIDO RECOMENDADOS Y OTROS ASUNTOS CONEXOS.

Se me ha explicado verbalmente toda la información específica relacionada  con el tratamiento ortodóncico que me ha sido recomendado.  La información hace referencia básicamente a los siguientes temas: Justificación científica de la realización del (los) procedimiento(s) que me ha(n) sido recomendado(s), preparación y condiciones previas del paciente para hacer viable la realización del (los) tratamiento(s) como estar libre de caries y enfermedad de las encías y haber visitado recientemente al Odontólogo para la limpieza general previa, mantenimiento de mis visitas periódicas a “Mi Odontólogo”; explicación sobre la metodología o la forma como se realiza el(los) procedimiento(s) recomendado(s), así como el haberme mostrado físicamente los aditamentos con los que se hará el tratamiento, el tiempo aproximado de duración y las actividades que se realizan en las distintas citas;  también las incomodidades que puede(n) producir dicho(s) procedimiento(s) como cierta sensibilidad de los dientes luego del cambio de los aparatos o la colocación o reposición de Brackets o auxiliares y las precauciones con la higiene oral.  Información general sobre los riesgos y complicaciones previstas. Los posibles y más importantes beneficios del tratamiento, así como el plan de mi tratamiento me fue explicado con detalle y en términos que comprendí luego de la explicación que me hizo el profesional y su personal auxiliar.

Mediante la presente, yo como paciente y/o el representante confirma que: se me han comunicado las principales consideraciones y los principales riesgos del tratamiento de Ortodoncia.  He leído y entendido este documento y el anexo de diagnóstico, objetivos y plan de tratamiento y comprendo que además pueden existir otros problemas que ocurren con menos frecuencia o son menos severos.

Se me ha expuesto el tratamiento de Ortodoncia para solucionar mi anomalía y se me ha presentado información para ayudarme a tomar mi decisión, otorgándoseme la oportunidad de aclarar todos los cuestionamientos sobre el tratamiento propuesto y la información contenida en este documento.  Por consiguiente consiento como acudiente y asiento como acudiente a que se me proporcione el tratamiento de Ortodoncia. Declaro (declaramos) que autorizo (autorizamos) al Ortodoncista y al personal auxiliar respectivo a realizar todos los procedimientos conexos y complementarios con la atención principal que se ofrece y que he (hemos) aceptado voluntariamente.

Se me ha informado el valor del tratamiento y he convenido su forma de pago.  He firmado y conozco que debo cumplir las citas ortodóncicas asignadas y que en caso de inasistencia por un período de tres meses sin justa causa, se podrá dar por terminado el contrato de prestación de servicios profesionales.  Otra forma de terminación anticipada del tratamiento se deberá al no pago de los honorarios profesionales acordados, no dándose lugar a restitución.  Así mismo, acepto pagar los cargos adicionales por pérdida de aparatos, Brackets o auxiliares, Brackets o auxiliares rotos por mal uso o mal trato y los que no adapten por su uso inconstante. Así mismo por la perdida y/o rotura de los auxiliares usados para mi tratamiento como botones, brackets, resinas, minimplantes u otros que se me coloquen o me indique usar.

Igualmente, SI (  ) NO (  ) autorizo el uso del expediente con sus registros y exámenes de Ortodoncia con fines de consultas profesionales, investigación, educación o publicación en revistas profesionales."""

PLANTILLAS_NUEVAS = [
    {
        "nombre": "Ortodoncia — Consentimiento General (Alineadores, Brackets y auxiliares)",
        "tipo": "GENERAL",
        "texto": TEXTO_ORTODONCIA_GENERAL,
        "requiere_autorizacion_expediente": True,
    },
    {
        "nombre": "Ortodoncia Interceptiva — Tratamiento Temprano",
        "tipo": "GENERAL",
        "texto": TEXTO_ORTODONCIA_INTERCEPTIVA,
        "requiere_autorizacion_expediente": True,
    },
]


class Command(BaseCommand):
    help = "Carga las plantillas de consentimiento de Clinica R y desactiva las anteriores (sin borrar nada)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Solo muestra que haria, no escribe en la base de datos.")

    def handle(self, *args, **options):
        dry = options["dry_run"]
        User = get_user_model()
        admin_user = User.objects.filter(is_superuser=True).order_by("id").first()
        nombres_nuevos = [datos["nombre"] for datos in PLANTILLAS_NUEVAS]

        with transaction.atomic():
            sid = transaction.savepoint()

            self.stdout.write(self.style.WARNING("== Paso 1: desactivar plantillas actuales (activa=False, sin borrar) =="))
            # Se excluyen explicitamente los nombres de las plantillas nuevas de Clinica R:
            # en una re-ejecucion de este comando (idempotente), esas ya podrian estar activas
            # de una corrida anterior y NO deben desactivarse a si mismas.
            activas = PlantillaConsentimiento.objects.filter(activa=True).exclude(nombre__in=nombres_nuevos)
            if not activas.exists():
                self.stdout.write("  (ninguna plantilla antigua activa por desactivar)")
            for p in activas:
                self.stdout.write(f"  - Desactivando: {p.nombre!r} (v{p.version})")
                if not dry:
                    p.activa = False
                    p.save(update_fields=["activa"])

            self.stdout.write(self.style.WARNING("== Paso 2: crear o asegurar activas las nuevas plantillas de Clinica R =="))
            # IMPORTANTE: el modelo PlantillaConsentimiento tiene 'nombre' con unique=True
            # a nivel de campo (ademas del unique_together con 'version'), por lo tanto
            # NUNCA puede existir mas de una fila con el mismo nombre, sin importar la
            # version. Por eso este comando identifica cada plantilla por su 'nombre'
            # exacto y es idempotente: si ya existe, la reactiva/actualiza en el mismo
            # lugar en vez de intentar crear una fila nueva con ese nombre.
            for datos in PLANTILLAS_NUEVAS:
                existente = PlantillaConsentimiento.objects.filter(nombre=datos["nombre"]).first()
                if existente:
                    cambios = []
                    if not existente.activa:
                        cambios.append("activa=True")
                    if existente.texto != datos["texto"]:
                        cambios.append("texto actualizado")
                    if existente.requiere_autorizacion_expediente != datos["requiere_autorizacion_expediente"]:
                        cambios.append("requiere_autorizacion_expediente actualizado")
                    if cambios:
                        self.stdout.write(f"  - Ya existía: {datos['nombre']!r} -> {', '.join(cambios)}")
                        if not dry:
                            existente.activa = True
                            existente.texto = datos["texto"]
                            existente.requiere_autorizacion_expediente = datos["requiere_autorizacion_expediente"]
                            existente.save(update_fields=["activa", "texto", "requiere_autorizacion_expediente"])
                    else:
                        self.stdout.write(f"  - Ya existía y estaba al día (sin cambios): {datos['nombre']!r}")
                else:
                    self.stdout.write(f"  - Creando: {datos['nombre']!r} (v1)")
                    if not dry:
                        PlantillaConsentimiento.objects.create(
                            nombre=datos["nombre"],
                            tipo=datos["tipo"],
                            texto=datos["texto"],
                            version=1,
                            requiere_autorizacion_expediente=datos["requiere_autorizacion_expediente"],
                            activa=True,
                            creado_por=admin_user,
                        )

            if dry:
                # --dry-run: revertimos cualquier escritura (no debería haber ninguna,
                # pero el savepoint garantiza que --dry-run nunca deja rastro en BD)
                transaction.savepoint_rollback(sid)
                self.stdout.write(self.style.NOTICE("Modo --dry-run: no se escribio nada en la base de datos."))
            else:
                transaction.savepoint_commit(sid)
                self.stdout.write(self.style.SUCCESS("Listo. Plantillas anteriores desactivadas (conservadas) y nuevas plantillas activas."))
