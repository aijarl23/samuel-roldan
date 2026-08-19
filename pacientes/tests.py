from django.contrib.auth.models import User, Group
from django.core.cache import cache
from django.test import TestCase

from accounts.roles import configurar_grupos
from .models import Paciente


class PermisosPacienteTests(TestCase):
    """Un rol sin permiso debe quedar bloqueado en el backend, no solo en la UI."""

    def setUp(self):
        cache.clear()
        od, aux = configurar_grupos()
        self.admin = User.objects.create_superuser('admin_t', 'a@x.co', 'x')
        self.odontologo = User.objects.create_user('od_t', password='x')
        self.odontologo.groups.set([od])
        self.auxiliar = User.objects.create_user('aux_t', password='x')
        self.auxiliar.groups.set([aux])
        self.sin_rol = User.objects.create_user('sinrol_t', password='x')
        self.paciente = Paciente.objects.create(
            documento='T0001', tipo_documento='CC', nombres='Ana', apellidos='Gómez')

    def test_anonimo_redirige_a_login(self):
        r = self.client.get(f'/pacientes/{self.paciente.pk}/')
        self.assertEqual(r.status_code, 302)
        self.assertIn('/accounts/login', r.url)

    def test_admin_odontologo_auxiliar_pueden_ver_paciente(self):
        for user in (self.admin, self.odontologo, self.auxiliar):
            self.client.force_login(user)
            r = self.client.get(f'/pacientes/{self.paciente.pk}/')
            self.assertEqual(r.status_code, 200, f'{user.username} debería poder ver el paciente')

    def test_usuario_sin_rol_bloqueado(self):
        self.client.force_login(self.sin_rol)
        r = self.client.get('/pacientes/')
        self.assertEqual(r.status_code, 403)

    def test_auxiliar_puede_crear_paciente(self):
        self.client.force_login(self.auxiliar)
        r = self.client.post('/pacientes/nuevo/panel/', {
            'tipo_documento': 'CC', 'documento': 'T0002', 'nombres': 'Luis', 'apellidos': 'Ruiz',
        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Paciente.objects.filter(documento='T0002').exists())

    def test_is_staff_se_asigna_automaticamente_al_grupo(self):
        u = User.objects.create_user('nuevo_od', password='x')
        u.groups.set([Group.objects.get(name='Odontologo')])
        u.refresh_from_db()
        self.assertTrue(u.is_staff, 'Sin is_staff, el permiso de modelo no se puede usar en /admin/')

    def test_editar_paciente_completo_via_admin(self):
        """El edit completo (EPS, antecedentes, acudiente) vive en /admin/;
        Auxiliar y Odontólogo deben poder usarlo porque tienen change_paciente."""
        self.client.force_login(self.auxiliar)
        r = self.client.get(f'/admin/pacientes/paciente/{self.paciente.pk}/change/')
        self.assertEqual(r.status_code, 200)
