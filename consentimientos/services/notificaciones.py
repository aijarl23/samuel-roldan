"""
Servicio de notificaciones: correo y WhatsApp (Twilio).
Falla silenciosamente con log de error para no bloquear el flujo principal.
"""
import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

logger = logging.getLogger(__name__)


def enviar_correo(consentimiento):
    paciente = consentimiento.paciente
    if not paciente.correo:
        logger.info('Correo: paciente sin correo registrado, omitiendo.')
        return False
    try:
        msg = EmailMessage(
            subject=f'Su consentimiento informado — {consentimiento.plantilla.nombre}',
            body=(f'Estimado/a {paciente.nombre_completo},\n\n'
                  f'Adjunto encontrará el consentimiento informado firmado para el procedimiento '
                  f'"{consentimiento.plantilla.nombre}", firmado el '
                  f'{consentimiento.fecha_firma.strftime("%d/%m/%Y")}.\n\n'
                  f'Conserve este documento como comprobante.\n\n'
                  f'Atentamente,\nConsultorio Odontológico Samuel Roldán'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[paciente.correo],
        )
        if consentimiento.pdf:
            msg.attach_file(consentimiento.pdf.path)
        msg.send()
        consentimiento.enviado_correo = True
        consentimiento.fecha_envio_correo = timezone.now()
        consentimiento.save(update_fields=['enviado_correo', 'fecha_envio_correo'])
        logger.info('Correo enviado a %s', paciente.correo)
        return True
    except Exception as e:
        logger.error('Error enviando correo a %s: %s', paciente.correo, e)
        return False


def enviar_whatsapp(consentimiento):
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        return False
    paciente = consentimiento.paciente
    tel = paciente.telefono or paciente.acudiente_telefono
    if not tel:
        return False
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        numero = f'whatsapp:+57{tel.replace(" ", "").replace("-", "")}'
        client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=numero,
            body=(f'Hola {paciente.nombres}, su consentimiento informado para '
                  f'"{consentimiento.plantilla.nombre}" ha sido registrado exitosamente '
                  f'el {consentimiento.fecha_firma.strftime("%d/%m/%Y")}.\n'
                  f'Si tiene dudas, comuníquese con el consultorio. '
                  f'Consultorio Odontológico Samuel Roldán.')
        )
        consentimiento.enviado_whatsapp = True
        consentimiento.fecha_envio_whatsapp = timezone.now()
        consentimiento.save(update_fields=['enviado_whatsapp', 'fecha_envio_whatsapp'])
        logger.info('WhatsApp enviado a %s', numero)
        return True
    except Exception as e:
        logger.error('Error enviando WhatsApp: %s', e)
        return False
