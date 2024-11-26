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


    def test_registration_form_invalid_missing_username(self):
        # Datos del formulario sin el campo "username"
        data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'Cliente',
        }
        response = self.client.post(reverse('Autenticacion'), data)

        # Verifica que la página permanece en el registro
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro/registro.html')

        # Verifica que se muestra el mensaje de error para el campo "username"
        self.assertContains(response, "Este campo es obligatorio.")

        # Verifica que el usuario no fue creado
        self.assertFalse(User.objects.filter(email='testuser@example.com').exists())
    
     
    def test_registration_form_invalid_missing_email(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'Cliente'
        }
        response = self.client.post(reverse('Autenticacion'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')
        
        
    def test_registration_form_invalid_missing_password(self):
        # Datos del formulario sin los campos de contraseña
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': '',
            'password2': '',
            'role': 'Cliente',
        }
        response = self.client.post(reverse('Autenticacion'), data)

        # Verifica que la página permanece en el registro
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro/registro.html')

        # Verifica que se muestra el mensaje de error para el campo de contraseña
        self.assertContains(response, "Este campo es obligatorio.")

        # Verifica que el usuario no fue creado
        self.assertFalse(User.objects.filter(username='testuser').exists())
        
        
    def test_registration_form_invalid_missing_role(self):
        # Datos del formulario sin el campo "role"
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('Autenticacion'), data)
        
        # Verifica que la página permanece en el registro
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro/registro.html')

        # Verifica que se muestra el mensaje de error para el campo "role"
        self.assertContains(response, "Este campo es obligatorio.")

        # Verifica que el usuario no fue creado
        self.assertFalse(User.objects.filter(username='testuser').exists())

    
    def test_registration_with_duplicate_username(self):
        # Crear el primer usuario
        data1 = {
            'username': 'duplicateuser',
            'email': 'user1@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'Cliente',
        }
        response1 = self.client.post(reverse('Autenticacion'), data1)
        self.assertEqual(response1.status_code, 302)  # Registro exitoso

        # Intentar registrar otro usuario con el mismo username
        data2 = {
            'username': 'duplicateuser',  # Nombre de usuario duplicado
            'email': 'user2@example.com',
            'password1': 'testpassword456',
            'password2': 'testpassword456',
            'role': 'Propietario',
        }
        response2 = self.client.post(reverse('Autenticacion'), data2)
        self.assertEqual(response2.status_code, 200)  # Permanece en la página de registro
        self.assertContains(response2, "Ya existe un usuario con este nombre.")  # Verifica el mensaje de error

        # Asegurarse de que solo hay un usuario con este nombre de usuario
        self.assertEqual(User.objects.filter(username='duplicateuser').count(), 1)
        
        
    def test_registration_form_invalid_duplicate_email(self):
        # Crear el primer usuario
        data1 = {
            'username': 'testuser1',
            'email': 'duplicate@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'Cliente'
        }
        response1 = self.client.post(reverse('Autenticacion'), data1)
        self.assertEqual(response1.status_code, 302)  # Registro exitoso
        
        # Intentar registrar otro usuario con el mismo email
        data2 = {
            'username': 'testuser2',
            'email': 'duplicate@example.com',  # Email duplicado
            'password1': 'testpassword456',
            'password2': 'testpassword456',
            'role': 'Propietario'
        }
        response2 = self.client.post(reverse('Autenticacion'), data2)
        self.assertEqual(response2.status_code, 200)  # Debe permanecer en la página de registro
        self.assertContains(response2, "Este correo electrónico ya está registrado. Por favor, utiliza otro.")

        # Asegurarse de que solo un usuario tiene este email
        self.assertEqual(User.objects.filter(email='duplicate@example.com').count(), 1)


    def test_post_registration_form_invalid_different_password(self):
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
        response = self.client.post(reverse('cerrar_sesion'))
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
        
    def test_login_valid_with_email(self):
        # Datos para iniciar sesión con el correo
        data = {
            'username_or_email': 'testuser@example.com',  # Correo del usuario
            'password': 'testpassword123'  # Contraseña válida
        }
        response = self.client.post(reverse('iniciar_sesion'), data)

        # Verifica que la respuesta redirige al "Home"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Home'))

        # Verifica que el usuario está autenticado
        self.assertTrue('_auth_user_id' in self.client.session)

