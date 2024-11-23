from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group


class CustomUserCreationFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Asegura que los grupos existen antes de las pruebas
        Group.objects.get_or_create(name='Propietario')
        Group.objects.get_or_create(name='Cliente')

    def test_get_registration_page(self):
        # Probar acceso a la página de registro
        response = self.client.get(reverse('Autenticacion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro/registro.html')

    def test_post_registration_form_valid(self):
        # Probar envío de formulario válido
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'Cliente'
        }
        response = self.client.post(reverse('Autenticacion'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después del registro
        self.assertRedirects(response, reverse('Home'))  # Redirección a 'Home'
        user = User.objects.get(username='testuser')
        self.assertTrue(user.groups.filter(name='Cliente').exists())  # Verifica grupo

    def test_post_registration_form_invalid(self):
        # Probar envío de formulario inválido (contraseñas no coinciden)
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
            'role': 'Cliente'
        }
        response = self.client.post(reverse('Autenticacion'), data)
        self.assertEqual(response.status_code, 200)  # Debe permanecer en la misma página
        self.assertTemplateUsed(response, 'registro/registro.html')
        self.assertContains(response, "Los dos campos de contraseña no coinciden.")  # Verifica el error


class AuthViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')

    def test_cerrar_sesion(self):
        # Probar cerrar sesión
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('cerrar_sesion'))
        self.assertEqual(response.status_code, 302)  # Redirección después de cerrar sesión
        self.assertRedirects(response, reverse('Home'))

    def test_iniciar_sesion_valid(self):
        # Probar inicio de sesión con datos válidos
        data = {
            'username_or_email': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('iniciar_sesion'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de inicio de sesión
        self.assertRedirects(response, reverse('Home'))

    def test_iniciar_sesion_invalid(self):
        # Probar inicio de sesión con datos inválidos
        data = {
            'username_or_email': 'wronguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('iniciar_sesion'), data)
        self.assertEqual(response.status_code, 302)  # Redirección a la misma página
        self.assertRedirects(response, reverse('iniciar_sesion'))
