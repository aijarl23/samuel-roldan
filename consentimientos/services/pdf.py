"""
Generación de PDF profesional con ReportLab.
ReportLab es la opción correcta para producción en Windows: sin dependencias de sistema.
"""
import io, base64, os, logging
from datetime import datetime
from xml.sax.saxutils import escape as _esc
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image, Table, TableStyle, HRFlowable)
from reportlab.lib import colors

logger = logging.getLogger(__name__)

AZUL = colors.HexColor('#26453F')
AZUL_OSC = colors.HexColor('#1B322D')
NARANJA = colors.HexColor('#A9C877')
GRIS = colors.HexColor('#8B978F')
NEGRO = colors.HexColor('#1C2B27')

# Recomendaciones de cuidado post-tratamiento para pacientes de Ortodoncia.
# Es contenido informativo (no legal), fijo para toda plantilla tipo
# ORTODONCIA — no se guarda en la base de datos porque no varía por paciente
# ni necesita congelarse como el texto del consentimiento.
CUIDADOS_ALINEADORES = (
    'Utilízalos según lo indicado. Evita consumir bebidas y comidas mientras tengas '
    'tus alineadores puestos. Evita exponerlos a temperaturas calientes.<br/>'
    'Lavado: en un vaso con agua fría agrega goticas de vinagre blanco o Corega tabs '
    'y sumerge tus alineadores; déjalos reposar de 20 a 30 minutos y enjuágalos con '
    'abundante agua. Puedes usar jabón de tocador para el lavado diario — evita '
    'lavarlos con crema dental, se pondrán opacos.'
)
CUIDADOS_BRACKETS = (
    '<b>1. Cepillo de ortodoncia:</b> utiliza tu cepillo de ortodoncia y crema dental '
    'para cepillarlos como normalmente lo haces.<br/>'
    '<b>2. Cepillo interdental:</b> pásalo por debajo del alambre de modo que roce tus '
    'dientes, con movimientos verticales, hasta que no quede ningún residuo — repítelo '
    'con cada diente.<br/>'
    '<b>3. Seda dental:</b> con ayuda del enhebrador pasa la seda por debajo del '
    'alambre, deslízala por cada diente con movimientos en zigzag.<br/>'
    '<b>4. Cera:</b> si sientes molestias, forma una bolita de cera y colócala sobre '
    'el bracket, evitando que roce con la piel.'
)
CUIDADOS_GENERALES = (
    'Durante todo tu tratamiento evita el consumo de alimentos duros (bombones, '
    'chicharrón, maní) y de alimentos cauchudos (chicles).'
)
CUIDADOS_CONTACTO = (
    'Ante cualquier duda o inconveniente, o si se te cae o rompe un bracket, avísanos '
    'de inmediato para que tu tratamiento no se retrase — WhatsApp 313 731 9827, '
    'Instagram @Samuelroldanr.'
)


def _firma_image(b64_data, ancho=6*cm, alto=2.5*cm):
    if not b64_data:
        return None
    try:
        raw = b64_data.split(',')[1] if ',' in b64_data else b64_data
        return Image(io.BytesIO(base64.b64decode(raw)), width=ancho, height=alto)
    except Exception:
        return None


def _encabezado_pie(canvas, doc):
    """Header y footer en cada página."""
    canvas.saveState()
    w, h = letter
    # Header
    canvas.setFillColor(AZUL_OSC)
    canvas.rect(0, h - 2.2*cm, w, 2.2*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 13)
    canvas.drawString(1.5*cm, h - 1.3*cm, 'CLÍNICA R · SAMUEL ROLDÁN')
    canvas.setFont('Helvetica', 8)
    canvas.drawString(1.5*cm, h - 1.9*cm, 'Sistema de Consentimientos Informados')
    canvas.setFont('Helvetica', 7)
    canvas.drawRightString(w - 1.5*cm, h - 1.5*cm, f'Pág. {doc.page}')
    # Footer
    canvas.setFillColor(GRIS)
    canvas.setFont('Helvetica', 6.5)
    canvas.drawString(1.5*cm, 0.7*cm,
        'Desarrollado por Solucionar Sistemas e Ingeniería SSI · Documento con validez legal')
    canvas.drawRightString(w - 1.5*cm, 0.7*cm,
        f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}')
    canvas.restoreState()


def generar(consentimiento):
    """
    Genera el PDF del consentimiento firmado.
    Retorna la ruta absoluta del archivo generado.
    """
    carpeta = os.path.join(settings.MEDIA_ROOT, 'consentimientos',
                           consentimiento.fecha_firma.strftime('%Y/%m') if consentimiento.fecha_firma
                           else 'borradores')
    os.makedirs(carpeta, exist_ok=True)
    nombre = f'consent_{consentimiento.id:06d}_{consentimiento.paciente.documento}.pdf'
    ruta = os.path.join(carpeta, nombre)

    doc = SimpleDocTemplate(ruta, pagesize=letter,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=3.2*cm, bottomMargin=2*cm)

    est = getSampleStyleSheet()
    T = lambda name, **kw: ParagraphStyle(name, parent=est['Normal'], **kw)

    s_titulo = T('T', fontSize=11, textColor=AZUL_OSC, fontName='Helvetica-Bold',
                 alignment=TA_CENTER, spaceAfter=4)
    s_seccion = T('S', fontSize=9, textColor=AZUL, fontName='Helvetica-Bold',
                  spaceBefore=8, spaceAfter=2)
    s_cuerpo = T('B', fontSize=8.5, alignment=TA_JUSTIFY, leading=13,
                 textColor=NEGRO, spaceAfter=4)
    s_meta = T('M', fontSize=8, textColor=GRIS, alignment=TA_LEFT)
    s_audit = T('A', fontSize=6.5, textColor=GRIS, alignment=TA_JUSTIFY, leading=9)
    s_firma_lbl = T('FL', fontSize=8, fontName='Helvetica-Bold', textColor=NEGRO)

    c = consentimiento
    p = c.paciente
    f = c.fecha_firma or c.creado
    od = c.odontologo

    el = []
    el.append(Paragraph(c.plantilla.nombre.upper(), s_titulo))
    el.append(HRFlowable(width='100%', thickness=1.5, color=NARANJA))
    el.append(Spacer(1, 0.3*cm))

    # Tabla de datos del paciente
    edad = f'({p.edad} años)' if p.edad else ''
    datos = [
        ['Paciente:', _esc(f'{p.nombre_completo} {edad}'),
         'Documento:', _esc(f'{p.tipo_documento} {p.documento}')],
        ['Odontólogo:', _esc(od.get_full_name() or od.username),
         'Fecha:', f.strftime('%d/%m/%Y %H:%M')],
        ['EPS:', _esc(p.eps) or '—', 'Ciudad:', _esc(p.ciudad) or 'Medellín'],
    ]
    tbl = Table(datos, colWidths=[2.8*cm, 6.5*cm, 2.8*cm, 4.8*cm])
    tbl.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), AZUL), ('TEXTCOLOR', (2,0), (2,-1), AZUL),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('TOPPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#F2EEE0')]),
    ]))
    el.append(tbl)
    el.append(Spacer(1, 0.4*cm))
    el.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#C3CDC6')))
    el.append(Spacer(1, 0.3*cm))

    # Texto del consentimiento
    texto = c.texto_generado or c.generar_texto()
    for linea in texto.split('\n'):
        linea = linea.strip()
        if not linea:
            el.append(Spacer(1, 0.2*cm))
        else:
            el.append(Paragraph(_esc(linea), s_cuerpo))

    # Autorización de expediente
    if c.plantilla.requiere_autorizacion_expediente and c.autoriza_expediente is not None:
        el.append(Spacer(1, 0.4*cm))
        el.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#C3CDC6')))
        si = '[X]' if c.autoriza_expediente else '[ ]'
        no = '[ ]' if c.autoriza_expediente else '[X]'
        el.append(Spacer(1, 0.2*cm))
        el.append(Paragraph(
            f'<b>Autorización uso del expediente con fines académicos y de investigación:</b> '
            f'SÍ {si}   NO {no}', s_cuerpo))

    # Firmas
    el.append(Spacer(1, 0.8*cm))
    el.append(HRFlowable(width='100%', thickness=1, color=AZUL))
    el.append(Spacer(1, 0.3*cm))

    firma_p_img = _firma_image(c.firma_paciente)
    firma_a_img = _firma_image(c.firma_acudiente) if p.es_menor else None

    f_lbl_p = _esc(f'{p.nombre_completo}\n{p.tipo_documento} {p.documento}\n'
               f'{"Paciente" if not p.es_menor else "Paciente (menor de edad)"}')
    f_lbl_a = _esc(f'{p.acudiente_nombre}\n{p.acudiente_tipo_doc} {p.acudiente_documento}\n'
               f'Acudiente / {p.acudiente_parentesco}') if p.es_menor else ''

    col_p = [firma_p_img or Paragraph('_' * 40, s_cuerpo),
             Paragraph(f_lbl_p, s_firma_lbl)]
    col_a = [firma_a_img or (Paragraph('_' * 40, s_cuerpo) if p.es_menor else Paragraph('', s_cuerpo)),
             Paragraph(f_lbl_a, s_firma_lbl)]

    tf = Table([[col_p[0], col_a[0]], [col_p[1], col_a[1]]],
               colWidths=[8.5*cm, 8.5*cm])
    tf.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), ('BOTTOMPADDING', (0,0), (-1,0), 4)]))
    el.append(tf)

    # Recomendaciones de cuidado (solo tratamientos de Ortodoncia)
    if c.plantilla.tipo == 'ORTODONCIA':
        el.append(Spacer(1, 0.7*cm))
        el.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#C3CDC6')))
        el.append(Spacer(1, 0.2*cm))
        el.append(Paragraph('CUIDA TU TRATAMIENTO', s_seccion))
        el.append(Paragraph('<b>Alineadores</b>', s_firma_lbl))
        el.append(Paragraph(CUIDADOS_ALINEADORES, s_cuerpo))
        el.append(Spacer(1, 0.15*cm))
        el.append(Paragraph('<b>Brackets</b>', s_firma_lbl))
        el.append(Paragraph(CUIDADOS_BRACKETS, s_cuerpo))
        el.append(Spacer(1, 0.15*cm))
        el.append(Paragraph(CUIDADOS_GENERALES, s_cuerpo))
        el.append(Spacer(1, 0.15*cm))
        el.append(Paragraph(CUIDADOS_CONTACTO, s_cuerpo))

    # Sello de auditoría
    el.append(Spacer(1, 0.8*cm))
    el.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#C3CDC6')))
    el.append(Spacer(1, 0.15*cm))
    el.append(Paragraph(
        f'SELLO DE AUDITORÍA ELECTRÓNICA — '
        f'Firmado: {f.strftime("%d/%m/%Y a las %H:%M:%S")} (Colombia UTC-5) — '
        f'IP: {_esc(c.ip_firma or "N/D")} — '
        f'Dispositivo: {_esc((c.dispositivo or "N/D")[:80])} — '
        f'Hash SHA-256: {c.hash_documento or "N/D"} — '
        f'Plantilla v{c.plantilla.version} — '
        f'Odontólogo responsable: {_esc(od.get_full_name() or od.username)}', s_audit))

    doc.build(el, onFirstPage=_encabezado_pie, onLaterPages=_encabezado_pie)
    logger.info('PDF generado: %s (%d bytes)', ruta, os.path.getsize(ruta))
    return ruta


