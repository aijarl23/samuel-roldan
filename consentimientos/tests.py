from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from accounts.roles import configurar_grupos
from pacientes.models import Paciente
from .models import Consentimiento, PlantillaConsentimiento
from .services import pdf as pdf_svc


FIRMA_PNG_VALIDA = ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')

class FlujoConsentimientoTests(TestCase):
    """Cubre el flujo completo: crear -> firmar -> PDF, y quién puede hacer qué."""

    def setUp(self):
        od, aux = configurar_grupos()
        self.odontologo = User.objects.create_user('od_c', password='x')
        self.odontologo.groups.set([od])
        self.auxiliar = User.objects.create_user('aux_c', password='x')
        self.auxiliar.groups.set([aux])
        self.paciente = Paciente.objects.create(
            documento='C0001', tipo_documento='CC', nombres='Sofía', apellidos='Torres')
        self.plantilla = PlantillaConsentimiento.objects.create(
            nombre='Plantilla de prueba', tipo='GENERAL',
            texto='Consentimiento de {{paciente}} para {{procedimiento}}.', activa=True)

    def test_auxiliar_puede_crear_consentimiento(self):
        self.client.force_login(self.auxiliar)
        r = self.client.post(f'/consentimientos/asistente/{self.paciente.pk}/',
                              {'plantilla_id': self.plantilla.pk})
        self.assertEqual(r.status_code, 200)
        c = Consentimiento.objects.get(paciente=self.paciente)
        self.assertEqual(c.estado, 'PENDIENTE')

    def test_auxiliar_bloqueado_de_firmar(self):
        c = Consentimiento.objects.create(
            paciente=self.paciente, plantilla=self.plantilla,
            odontologo=self.odontologo, creado_por=self.odontologo, estado='PENDIENTE')
        self.client.force_login(self.auxiliar)
        r_get = self.client.get(f'/consentimientos/firmar/{c.pk}/')
        self.assertEqual(r_get.status_code, 403)
        r_post = self.client.post(f'/consentimientos/firmar/{c.pk}/', {'firma_paciente': 'x' * 60})
        self.assertEqual(r_post.status_code, 403)
        c.refresh_from_db()
        self.assertEqual(c.estado, 'PENDIENTE', 'El auxiliar no debió poder firmar')

    def test_odontologo_puede_firmar_y_se_genera_pdf(self):
        c = Consentimiento.objects.create(
            paciente=self.paciente, plantilla=self.plantilla,
            odontologo=self.odontologo, creado_por=self.odontologo, estado='PENDIENTE')
        self.client.force_login(self.odontologo)
        r = self.client.post(f'/consentimientos/firmar/{c.pk}/',
                              {'firma_paciente': FIRMA_PNG_VALIDA}, follow=True)
        c.refresh_from_db()
        self.assertEqual(c.estado, 'FIRMADO')
        self.assertTrue(c.texto_generado)
        self.assertTrue(c.hash_documento)
        self.assertTrue(c.pdf)
        self.assertIsNotNone(c.fecha_firma)

        r_pdf = self.client.get(f'/consentimientos/{c.pk}/pdf/')
        self.assertEqual(r_pdf.status_code, 200)
        contenido = b''.join(r_pdf.streaming_content) if r_pdf.streaming else r_pdf.content
        self.assertEqual(contenido[:4], b'%PDF')

    def test_firma_con_formato_invalido_es_rechazada(self):
        c = Consentimiento.objects.create(
            paciente=self.paciente, plantilla=self.plantilla,
            odontologo=self.odontologo, creado_por=self.odontologo, estado='PENDIENTE')
        self.client.force_login(self.odontologo)
        self.client.post(f'/consentimientos/firmar/{c.pk}/', {'firma_paciente': 'x' * 60})
        c.refresh_from_db()
        self.assertEqual(c.estado, 'PENDIENTE', 'Una firma que no es imagen PNG no debe aceptarse')

    def test_menor_de_edad_requiere_firma_de_acudiente(self):
        menor = Paciente.objects.create(
            documento='C0002', tipo_documento='TI', nombres='Niño', apellidos='Prueba',
            es_menor=True, acudiente_nombre='Padre Prueba', acudiente_parentesco='Padre')
        c = Consentimiento.objects.create(
            paciente=menor, plantilla=self.plantilla,
            odontologo=self.odontologo, creado_por=self.odontologo, estado='PENDIENTE')
        self.client.force_login(self.odontologo)
        r = self.client.post(f'/consentimientos/firmar/{c.pk}/', {'firma_paciente': 'x' * 60})
        c.refresh_from_db()
        self.assertEqual(c.estado, 'PENDIENTE', 'Sin firma del acudiente no debe quedar firmado')

    def test_sin_rol_no_puede_ver_consentimiento(self):
        c = Consentimiento.objects.create(
            paciente=self.paciente, plantilla=self.plantilla,
            odontologo=self.odontologo, creado_por=self.odontologo, estado='PENDIENTE')
        sin_rol = User.objects.create_user('sinrol_c', password='x')
        self.client.force_login(sin_rol)
        r = self.client.get(f'/consentimientos/{c.pk}/')
        self.assertEqual(r.status_code, 403)

    def test_anonimo_no_puede_ver_pdf(self):
        c = Consentimiento.objects.create(
            paciente=self.paciente, plantilla=self.plantilla,
            odontologo=self.odontologo, creado_por=self.odontologo, estado='PENDIENTE')
        r = self.client.get(f'/consentimientos/{c.pk}/pdf/')
        self.assertEqual(r.status_code, 302)


class InmutabilidadConsentimientoTests(TestCase):
    """El documento firmado es legal: no puede alterarse por ninguna vía, ni /admin/."""

    def setUp(self):
        self.od = User.objects.create_user('od_i', password='x')
        self.p1 = Paciente.objects.create(documento='I0001', tipo_documento='CC', nombres='A', apellidos='B')
        self.p2 = Paciente.objects.create(documento='I0002', tipo_documento='CC', nombres='C', apellidos='D')
        self.plantilla = PlantillaConsentimiento.objects.create(
            nombre='Plantilla inmutable', tipo='GENERAL', texto='x', activa=True)
        self.c = Consentimiento.objects.create(
            paciente=self.p1, plantilla=self.plantilla, odontologo=self.od, creado_por=self.od,
            estado='FIRMADO', texto_generado='texto original', hash_documento='hash123')

    def test_no_permite_cambiar_paciente(self):
        self.c.paciente = self.p2
        with self.assertRaises(ValidationError):
            self.c.save()
        self.c.refresh_from_db()
        self.assertEqual(self.c.paciente_id, self.p1.pk)

    def test_no_permite_alterar_texto(self):
        self.c.texto_generado = 'texto ALTERADO'
        with self.assertRaises(ValidationError):
            self.c.save()

    def test_no_permite_desfirmar(self):
        self.c.estado = 'PENDIENTE'
        with self.assertRaises(ValidationError):
            self.c.save()

    def test_si_permite_anular(self):
        self.c.estado = 'ANULADO'
        self.c.save()  # no debe lanzar
        self.c.refresh_from_db()
        self.assertEqual(self.c.estado, 'ANULADO')

    def test_si_permite_notas_internas(self):
        self.c.notas_internas = 'nota administrativa'
        self.c.save()  # no debe lanzar
        self.c.refresh_from_db()
        self.assertEqual(self.c.notas_internas, 'nota administrativa')

    def test_admin_no_puede_reasignar_paciente_de_firmado(self):
        admin = User.objects.create_superuser('super_i', 'a@x.co', 'x')
        self.client.force_login(admin)
        r = self.client.post(f'/admin/consentimientos/consentimiento/{self.c.pk}/change/', {
            'paciente': self.p2.pk, 'plantilla': self.plantilla.pk, 'odontologo': self.od.pk,
            'estado': 'FIRMADO', 'notas_internas': '',
        })
        self.c.refresh_from_db()
        self.assertEqual(self.c.paciente_id, self.p1.pk, 'El admin no debe poder cambiar el paciente')


class PdfGeneracionTests(TestCase):
    """El PDF debe generarse incluso con datos maliciosos/atípicos, sin exponer un error 500."""

    def test_pdf_con_caracteres_especiales_y_campos_nulos(self):
        od = User.objects.create_user('od_pdf', password='x')
        p = Paciente.objects.create(
            documento='P0001', tipo_documento='CC', nombres='Test', apellidos='PDF',
            eps='EPS & Cía. <especial>')
        plantilla = PlantillaConsentimiento.objects.create(
            nombre='Plantilla PDF', tipo='GENERAL',
            texto='Texto con <etiquetas> & símbolos para {{paciente}}.', activa=True)
        c = Consentimiento.objects.create(
            paciente=p, plantilla=plantilla, odontologo=od, creado_por=od, estado='PENDIENTE')
        c.firma_paciente = 'x' * 60
        c.texto_generado = c.generar_texto()
        c.fecha_firma = timezone.now()
        c.ip_firma = None
        c.dispositivo = 'Mozilla/5.0 <script>alert(1)</script> & "raro"'
        c.estado = 'FIRMADO'
        c.save()

        ruta = pdf_svc.generar(c)
        with open(ruta, 'rb') as fh:
            self.assertEqual(fh.read(4), b'%PDF')
