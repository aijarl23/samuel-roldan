from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    ROL = [('ADMIN', 'Administrador'), ('ODONTOLOGO', 'Odontólogo'), ('AUXILIAR', 'Auxiliar')]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=12, choices=ROL, default='AUXILIAR')
    telefono = models.CharField(max_length=20, blank=True)
    firma_digital = models.TextField('Firma digital (PNG base64)', blank=True)
    tarjeta_profesional = models.CharField('Número tarjeta profesional', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f'{self.usuario.get_full_name() or self.usuario.username} — {self.get_rol_display()}'
