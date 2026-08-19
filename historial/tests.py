from django.contrib.auth.models import User
from django.test import TestCase

from accounts.roles import configurar_grupos
from pacientes.models import Paciente


class PermisosHistorialTests(TestCase):

    def setUp(self):
        od, aux = configurar_grupos()
        self.odontologo = User.objects.create_user('od_h', password='x')
        self.odontologo.groups.set([od])
        self.auxiliar = User.objects.create_user('aux_h', password='x')
        self.auxiliar.groups.set([aux])
        self.sin_rol = User.objects.create_user('sinrol_h', password='x')
        self.paciente = Paciente.objects.create(
            documento='H0001', tipo_documento='CC', nombres='Marta', apellidos='Vélez')

    def test_odontologo_y_auxiliar_ven_historial(self):
        for user in (self.odontologo, self.auxiliar):
            self.client.force_login(user)
            r = self.client.get(f'/historial/paciente/{self.paciente.pk}/')
            self.assertEqual(r.status_code, 200, f'{user.username} debería poder ver el historial')

    def test_sin_rol_bloqueado(self):
        self.client.force_login(self.sin_rol)
        r = self.client.get(f'/historial/paciente/{self.paciente.pk}/')
        self.assertEqual(r.status_code, 403)

    def test_anonimo_redirige_a_login(self):
        r = self.client.get(f'/historial/paciente/{self.paciente.pk}/')
        self.assertEqual(r.status_code, 302)

    def test_odontologo_puede_registrar_evolucion_auxiliar_no(self):
        from historial.models import FichaClinica
        self.client.force_login(self.odontologo)
        self.client.get(f'/historial/paciente/{self.paciente.pk}/')  # crea la FichaClinica
        ficha = FichaClinica.objects.get(paciente=self.paciente)

        r_od = self.client.get('/admin/historial/evolucionclinica/add/')
        self.assertEqual(r_od.status_code, 200)

        self.client.force_login(self.auxiliar)
        r_aux = self.client.get('/admin/historial/evolucionclinica/add/')
        self.assertEqual(r_aux.status_code, 403)
