"""
Servicio de almacenamiento en Google Drive institucional.
Estructura: RaizConsultorio / Año / Mes / CC-NombrePaciente / archivo.pdf
"""
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

MESES = {1:'01-Enero',2:'02-Febrero',3:'03-Marzo',4:'04-Abril',5:'05-Mayo',
         6:'06-Junio',7:'07-Julio',8:'08-Agosto',9:'09-Septiembre',
         10:'10-Octubre',11:'11-Noviembre',12:'12-Diciembre'}


def _build_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        cred_path = settings.GOOGLE_DRIVE_CREDENTIALS
        if not cred_path or not os.path.exists(cred_path):
            logger.warning('Drive: credenciales no encontradas en %s', cred_path)
            return None
        creds = service_account.Credentials.from_service_account_file(
            cred_path, scopes=['https://www.googleapis.com/auth/drive'])
        return build('drive', 'v3', credentials=creds, cache_discovery=False)
    except Exception as e:
        logger.error('Drive: error al construir servicio: %s', e)
        return None


def _get_or_create_folder(service, name, parent_id):
    q = (f"name='{name}' and mimeType='application/vnd.google-apps.folder' "
         f"and '{parent_id}' in parents and trashed=false")
    res = service.files().list(q=q, fields='files(id)', pageSize=1).execute().get('files', [])
    if res:
        return res[0]['id']
    meta = {'name': name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_id]}
    return service.files().create(body=meta, fields='id').execute()['id']


def subir_pdf(consentimiento, ruta_pdf_local):
    """
    Sube el PDF firmado a Drive en la estructura organizada.
    Retorna la URL de visualización o cadena vacía si Drive no está configurado.
    """
    service = _build_service()
    raiz = settings.GOOGLE_DRIVE_FOLDER_ID
    if not service or not raiz:
        logger.info('Drive: no configurado, omitiendo subida.')
        return ''

    try:
        from googleapiclient.http import MediaFileUpload
        dt = consentimiento.fecha_firma or consentimiento.creado
        p = consentimiento.paciente

        folder_anio = _get_or_create_folder(service, str(dt.year), raiz)
        folder_mes = _get_or_create_folder(service, MESES[dt.month], folder_anio)
        folder_pac = _get_or_create_folder(service,
            f'{p.documento}-{p.apellidos}_{p.nombres}', folder_mes)

        nombre_archivo = (f'{dt.strftime("%Y%m%d_%H%M")}_'
                          f'{consentimiento.plantilla.tipo}_'
                          f'{p.documento}.pdf')
        media = MediaFileUpload(ruta_pdf_local, mimetype='application/pdf', resumable=True)
        archivo = service.files().create(
            body={'name': nombre_archivo, 'parents': [folder_pac]},
            media_body=media, fields='id,webViewLink').execute()

        url = archivo.get('webViewLink', '')
        logger.info('Drive: PDF subido correctamente. URL: %s', url)
        return url

    except Exception as e:
        logger.error('Drive: error al subir PDF: %s', e)
        return ''
