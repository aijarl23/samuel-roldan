from django.db import models
from django.urls import reverse
from auditlog.registry import auditlog


class Paciente(models.Model):
    TIPO_DOC = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('PA', 'Pasaporte'),
        ('RC', 'Registro civil'),
        ('NIT', 'NIT'),
    ]
    SEXO = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    GRUPO_SANGRE = ['A+','A-','B+','B-','AB+','AB-','O+','O-','?']

    # Identificación
    tipo_documento = models.CharField('Tipo de documento', max_length=3, choices=TIPO_DOC, default='CC')
    documento = models.CharField('Número de documento', max_length=20, unique=True, db_index=True)
    nombres = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO, blank=True)
    grupo_sanguineo = models.CharField('Grupo sanguíneo', max_length=3, blank=True,
        choices=[(g, g) for g in GRUPO_SANGRE])
    foto = models.ImageField(upload_to='pacientes/fotos/', blank=True, null=True)

    # Contacto
    telefono = models.CharField('Teléfono / Celular', max_length=20, blank=True)
    correo = models.EmailField('Correo electrónico', blank=True)
    direccion = models.CharField('Dirección', max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True, default='Medellín')
    eps = models.CharField('EPS / Aseguradora', max_length=100, blank=True)
    ocupacion = models.CharField('Ocupación', max_length=100, blank=True)

    # Acudiente
    es_menor = models.BooleanField('¿Es menor de edad?', default=False)
    acudiente_nombre = models.CharField('Nombre del acudiente', max_length=200, blank=True)
    acudiente_tipo_doc = models.CharField('Tipo de doc. acudiente', max_length=3,
        choices=TIPO_DOC, blank=True)
    acudiente_documento = models.CharField('Documento del acudiente', max_length=20, blank=True)
    acudiente_parentesco = models.CharField('Parentesco', max_length=50, blank=True)
    acudiente_telefono = models.CharField('Teléfono del acudiente', max_length=20, blank=True)

    # Antecedentes médicos
    alergias = models.TextField('Alergias conocidas', blank=True)
    medicamentos = models.TextField('Medicamentos actuales', blank=True)
    antecedentes = models.TextField('Antecedentes médicos relevantes', blank=True)
    observaciones = models.TextField('Observaciones adicionales', blank=True)

    activo = models.BooleanField('Paciente activo', default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellidos', 'nombres']
        indexes = [models.Index(fields=['documento']), models.Index(fields=['apellidos', 'nombres'])]

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None
        from datetime import date
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def get_absolute_url(self):
        return reverse('pacientes:detalle', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.nombre_completo} ({self.tipo_documento} {self.documento})'


auditlog.register(Paciente)
