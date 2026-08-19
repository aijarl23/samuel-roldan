from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase


class LoginThrottleTests(TestCase):

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user('throttle_u', password='RealPass123!')

    def tearDown(self):
        cache.clear()

    def test_bloquea_tras_varios_intentos_fallidos(self):
        for _ in range(5):
            self.client.post('/accounts/login/', {'username': 'throttle_u', 'password': 'mala'})
        r = self.client.post('/accounts/login/', {'username': 'throttle_u', 'password': 'RealPass123!'})
        self.assertContains(r, 'Demasiados intentos', status_code=200)

    def test_login_correcto_funciona_sin_intentos_previos(self):
        r = self.client.post('/accounts/login/', {'username': 'throttle_u', 'password': 'RealPass123!'})
        self.assertEqual(r.status_code, 302)

    def test_login_exitoso_limpia_el_contador(self):
        for _ in range(3):
            self.client.post('/accounts/login/', {'username': 'throttle_u', 'password': 'mala'})
        r = self.client.post('/accounts/login/', {'username': 'throttle_u', 'password': 'RealPass123!'})
        self.assertEqual(r.status_code, 302)


class SesionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('sesion_u', password='x')

    def test_logout_invalida_la_sesion(self):
        self.client.force_login(self.user)
        self.client.post('/accounts/logout/')
        r = self.client.get('/')
        self.assertEqual(r.status_code, 302)
        self.assertIn('/accounts/login', r.url)

    def test_anonimo_no_accede_a_ninguna_ruta_privada(self):
        for url in ['/', '/pacientes/', '/admin/']:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 302, f'{url} debería redirigir a login')
