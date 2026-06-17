from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from pacientes.models import Paciente


class FichaClinica(models.Model):
    """Historia clínica base del paciente. Una por paciente."""
    paciente = models.OneToOneField(Paciente, on_delete=models.PROTECT, related_name='ficha')
    odontologo_principal = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
        related_name='fichas_a_cargo', verbose_name='Odontólogo principal')

    # Motivo de consulta
    motivo_consulta = models.TextField('Motivo de consulta inicial', blank=True)
    enfermedad_actual = models.TextField('Descripción de la enfermedad actual', blank=True)

    # Antecedentes específicos odontológicos
    ultima_visita_odontologo = models.DateField('Última visita al odontólogo', null=True, blank=True)
    tratamientos_previos = models.TextField('Tratamientos odontológicos previos', blank=True)
    higiene_oral = models.CharField('Frecuencia de cepillado', max_length=100, blank=True)
    usa_seda = models.BooleanField('Usa seda dental', default=False)
    usa_enjuague = models.BooleanField('Usa enjuague bucal', default=False)

    # Hábitos parafuncionales
    bruxismo = models.BooleanField('Bruxismo (rechinar dientes)', default=False)
    succion_digital = models.BooleanField('Succión digital', default=False)
    onicofagia = models.BooleanField('Onicofagia (comerse las uñas)', default=False)
    habitos_descripcion = models.TextField('Descripción de otros hábitos', blank=True)

    # Examen extraoral
    examen_extraoral = models.TextField('Examen extraoral', blank=True)
    examen_intraoral = models.TextField('Examen intraoral', blank=True)
    tejidos_blandos = models.TextField('Tejidos blandos', blank=True)

    # Plan de tratamiento global
    diagnostico = models.TextField('Diagnóstico', blank=True)
    plan_tratamiento = models.TextField('Plan de tratamiento', blank=True)
    pronostico = models.TextField('Pronóstico', blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
        related_name='fichas_creadas')

    class Meta:
        verbose_name = 'Ficha clínica'
        verbose_name_plural = 'Fichas clínicas'

    def __str__(self):
        return f'Historia clínica — {self.paciente.nombre_completo}'


class EvolucionClinica(models.Model):
    """Registro de cada cita / evolución clínica."""
    ficha = models.ForeignKey(FichaClinica, on_delete=models.PROTECT, related_name='evoluciones')
    odontologo = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Odontólogo')
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_proxima_cita = models.DateField('Próxima cita', null=True, blank=True)

    procedimiento = models.CharField('Procedimiento realizado', max_length=200)
    descripcion = models.TextField('Descripción detallada')
    materiales_usados = models.TextField('Materiales utilizados', blank=True)
    dientes_tratados = models.CharField('Dientes tratados (ej: 11, 12, 21)', max_length=100, blank=True)

    valor_cobrado = models.DecimalField('Valor cobrado (COP)', max_digits=12, decimal_places=0,
        null=True, blank=True)
    observaciones = models.TextField('Observaciones / Indicaciones al paciente', blank=True)

    class Meta:
        verbose_name = 'Evolución clínica'
        verbose_name_plural = 'Evoluciones clínicas'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.procedimiento} — {self.fecha.strftime("%d/%m/%Y")} — {self.ficha.paciente.nombre_completo}'


class Odontograma(models.Model):
    """Odontograma simplificado en formato JSON por diente."""
    ESTADO_DIENTE = [
        ('S', 'Sano'), ('C', 'Caries'), ('O', 'Obturado'), ('E', 'Extraído'),
        ('P', 'Puente'), ('I', 'Implante'), ('A', 'Ausente congénito'),
    ]
    ficha = models.ForeignKey(FichaClinica, on_delete=models.PROTECT, related_name='odontogramas')
    fecha = models.DateField(auto_now_add=True)
    odontologo = models.ForeignKey(User, on_delete=models.PROTECT)
    datos = models.JSONField('Datos del odontograma',
        default=dict, help_text='Mapa {numero_diente: {estado, notas, caras_afectadas}}')
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Odontograma'
        verbose_name_plural = 'Odontogramas'
        ordering = ['-fecha']

    def __str__(self):
        return f'Odontograma {self.fecha} — {self.ficha.paciente.nombre_completo}'


auditlog.register(FichaClinica)
auditlog.register(EvolucionClinica)
auditlog.register(Odontograma)
