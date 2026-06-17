import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from auditlog.registry import auditlog
from pacientes.models import Paciente


class PlantillaConsentimiento(models.Model):
    PROCEDIMIENTO = [
        ('ORTODONCIA', 'Ortodoncia'),
        ('ENDODONCIA', 'Endodoncia'),
        ('EXODONCIA', 'Exodoncia'),
        ('IMPLANTE', 'Implante dental'),
        ('CIRUGIA', 'Cirugía oral'),
        ('PERIODONCIA', 'Periodoncia'),
        ('PROSTODONCIA', 'Prostodoncia'),
        ('BLANQUEAMIENTO', 'Blanqueamiento dental'),
        ('GENERAL', 'Procedimiento general'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=150, unique=True)
    tipo = models.CharField(max_length=20, choices=PROCEDIMIENTO, default='GENERAL')
    texto = models.TextField(
        'Texto legal del consentimiento',
        help_text='Variables disponibles: {{paciente}}, {{documento}}, {{fecha}}, {{odontologo}}, {{procedimiento}}')
    version = models.PositiveSmallIntegerField('Versión', default=1)
    requiere_autorizacion_expediente = models.BooleanField('Incluir casilla autorización expediente', default=True)
    activa = models.BooleanField('Activa', default=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Plantilla de consentimiento'
        verbose_name_plural = 'Plantillas de consentimiento'
        ordering = ['nombre']
        unique_together = [('nombre', 'version')]

    def __str__(self):
        return f'{self.nombre} v{self.version}'


class Consentimiento(models.Model):
    ESTADO = [
        ('BORRADOR', 'Borrador'),
        ('PENDIENTE', 'Pendiente de firma'),
        ('FIRMADO', 'Firmado'),
        ('ANULADO', 'Anulado'),
    ]
    # Relaciones
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='consentimientos')
    plantilla = models.ForeignKey(PlantillaConsentimiento, on_delete=models.PROTECT)
    odontologo = models.ForeignKey(User, on_delete=models.PROTECT,
        related_name='consentimientos_como_odontologo', verbose_name='Odontólogo responsable')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
        related_name='consentimientos_creados')

    estado = models.CharField(max_length=10, choices=ESTADO, default='PENDIENTE', db_index=True)
    texto_generado = models.TextField('Texto del consentimiento al momento de firmar', blank=True)
    autoriza_expediente = models.BooleanField('Autoriza uso del expediente', null=True, blank=True)

    # Firmas (PNG en base64 del canvas)
    firma_paciente = models.TextField(blank=True)
    firma_acudiente = models.TextField(blank=True)

    # Auditoría forense
    fecha_firma = models.DateTimeField('Fecha y hora de firma', null=True, blank=True, db_index=True)
    ip_firma = models.GenericIPAddressField('IP de firma', null=True, blank=True)
    dispositivo = models.CharField('User-Agent del dispositivo', max_length=512, blank=True)
    hash_documento = models.CharField('Hash SHA-256 de integridad', max_length=64, blank=True)

    # Archivos y envíos
    pdf = models.FileField(upload_to='consentimientos/%Y/%m/', blank=True)
    drive_url = models.URLField('Enlace Google Drive', blank=True)
    enviado_correo = models.BooleanField('Enviado por correo', default=False)
    enviado_whatsapp = models.BooleanField('Enviado por WhatsApp', default=False)
    fecha_envio_correo = models.DateTimeField(null=True, blank=True)
    fecha_envio_whatsapp = models.DateTimeField(null=True, blank=True)

    notas_internas = models.TextField('Notas internas (no visibles para el paciente)', blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consentimiento'
        verbose_name_plural = 'Consentimientos'
        ordering = ['-creado']
        indexes = [
            models.Index(fields=['paciente', 'estado']),
            models.Index(fields=['fecha_firma']),
        ]

    def generar_texto(self):
        """Interpola variables en el texto de la plantilla."""
        from django.utils import timezone
        texto = self.plantilla.texto
        reemplazos = {
            '{{paciente}}': self.paciente.nombre_completo,
            '{{documento}}': f'{self.paciente.tipo_documento} {self.paciente.documento}',
            '{{fecha}}': timezone.localdate().strftime('%d/%m/%Y'),
            '{{odontologo}}': self.odontologo.get_full_name() or self.odontologo.username,
            '{{procedimiento}}': self.plantilla.nombre,
        }
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
        return texto

    def calcular_hash(self):
        """SHA-256 sobre datos inmutables del consentimiento."""
        base = (f'{self.paciente.documento}|{self.plantilla_id}|{self.plantilla.version}|'
                f'{self.fecha_firma}|{self.ip_firma}|{self.firma_paciente[:100]}')
        return hashlib.sha256(base.encode('utf-8')).hexdigest()

    def get_absolute_url(self):
        return reverse('consentimientos:detalle', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.plantilla.nombre} — {self.paciente.nombre_completo} [{self.get_estado_display()}]'


auditlog.register(Consentimiento, exclude_fields=['firma_paciente', 'firma_acudiente'])
