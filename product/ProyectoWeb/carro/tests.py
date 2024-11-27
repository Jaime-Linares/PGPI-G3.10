from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from catalogoViviendas.models import Vivienda
from carro.carro import Carro
from carro.models import Carro as CarroModel
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AnonymousUser
from carro.views import detalle_carro,eliminar_reserva_carro
from django.urls import reverse


from django.contrib.auth.models import AnonymousUser

class CarroUnauthenticatedTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


    def test_carro_invalid_usuario_no_autenticado(self):
        # Crear una instancia de Carro con un usuario no autenticado
        request = self.factory.get("/")
        request.user = AnonymousUser()  # Usuario no autenticado
        carro = Carro(request)

        # Verificar que el carro no tiene funcionalidad para usuarios no autenticados
        with self.assertRaises(AttributeError):
            carro.agregar_reserva(None, "2024-01-01", "2024-01-10", 900)


    def test_detalle_carro_invalid_usuario_no_autenticado(self):
        # Crear una solicitud para la vista detalle_carro
        request = self.factory.get("/carro/detalle/")
        request.user = AnonymousUser()  # Usuario no autenticado

        # Llamar a la vista
        response = detalle_carro(request)

        # Verificar que el usuario no autenticado es redirigido al login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))
    
    
    def test_invalid_eliminar_reserva_usuario_no_autenticado(self):
        # Crear una solicitud POST para eliminar la reserva
        request = self.factory.post(reverse('carro:eliminar'))
        request.user = AnonymousUser()  # Usuario no autenticado

        # Llamar a la vista eliminar_reserva_carro
        response = eliminar_reserva_carro(request)

        # Verificar que el usuario no autenticado es redirigido al login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class CarroClassTests(TestCase):
    def setUp(self):
        # Crear un usuario para los tests
        self.usuario = User.objects.create_user(username="testuser", password="testpassword123")
        self.factory = RequestFactory()

        # Crear una vivienda de prueba
        self.vivienda = Vivienda.objects.create(
            propietario=self.usuario,
            nombre="Casa Test",
            descripcion="Casa para pruebas",
            ubicacion="Calle Falsa",
            precio_por_dia=100.00,
            imagen=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )


    def test_valid_agregar_reserva(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Agregar una reserva
        carro.agregar_reserva(self.vivienda, "2024-01-01", "2024-01-10", 900)

        # Verificar los valores de la reserva
        self.assertEqual(carro.carro_usuario.vivienda, self.vivienda)
        self.assertEqual(str(carro.carro_usuario.fecha_inicio), "2024-01-01")
        self.assertEqual(str(carro.carro_usuario.fecha_fin), "2024-01-10")
        self.assertEqual(carro.carro_usuario.precio_total, 900)


    def test_valid_reserva_existente(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Sin reservas
        self.assertFalse(carro.reserva_existente())

        # Agregar una reserva
        carro.agregar_reserva(self.vivienda, "2024-01-01", "2024-01-10", 900)
        self.assertTrue(carro.reserva_existente())


    def test_valid_obtener_reserva(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Sin reservas
        self.assertIsNone(carro.obtener_reserva())

        # Agregar una reserva
        carro.agregar_reserva(self.vivienda, "2024-01-01", "2024-01-10", 900)

        # Verificar los valores obtenidos
        reserva = carro.obtener_reserva()
        self.assertEqual(reserva["vivienda"], self.vivienda)
        self.assertEqual(reserva["fecha_inicio"], carro.carro_usuario.fecha_inicio)
        self.assertEqual(reserva["fecha_fin"], carro.carro_usuario.fecha_fin)
        self.assertEqual(reserva["precio_total"], carro.carro_usuario.precio_total)
        

    def test_valid_ver_detalles_carro(self):
        # Iniciar sesión con el usuario
        self.client.login(username="testuser", password="testpassword123")

        # Hacer una solicitud GET a la vista detalle_carro
        response = self.client.get(reverse('carro:detalle'))

        # Verificar que la respuesta es correcta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carro/detalle.html')

        # Verificar que el contexto no contiene una reserva (carro vacío)
        self.assertIn("reserva", response.context)
        self.assertIsNone(response.context["reserva"])


    def test_valid_eliminar_reserva_usuario(self):
        # Iniciar sesión con el usuario
        self.client.login(username="testuser", password="testpassword123")

        # Agregar una reserva al carrito
        carro_model, _ = CarroModel.objects.get_or_create(usuario=self.usuario)
        carro_model.vivienda = self.vivienda
        carro_model.fecha_inicio = "2024-01-01"
        carro_model.fecha_fin = "2024-01-10"
        carro_model.precio_total = 900
        carro_model.save()

        # Verificar que la reserva existe antes de eliminarla
        self.assertIsNotNone(carro_model.vivienda)

        # Hacer una solicitud POST para eliminar la reserva
        response = self.client.post(reverse('carro:eliminar'))

        # Verificar que la respuesta redirige al detalle del carrito
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('carro:detalle'))

        # Verificar que la reserva ha sido eliminada
        carro_model.refresh_from_db()  # Actualizar el objeto desde la base de datos
        self.assertIsNone(carro_model.vivienda)

   
    def test_valid_limpiar_carro(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Agregar una reserva
        carro.agregar_reserva(self.vivienda, "2024-01-01", "2024-01-10", 900)

        # Confirmar que la reserva existe antes de eliminarla
        self.assertTrue(carro.reserva_existente())

        # Llamar al método para limpiar el carrito
        carro.limpiar_carro()

        # Verificar que la reserva fue eliminada
        self.assertFalse(carro.reserva_existente())
        self.assertIsNone(carro.carro_usuario.vivienda)
        self.assertIsNone(carro.carro_usuario.fecha_inicio)
        self.assertIsNone(carro.carro_usuario.fecha_fin)
        self.assertIsNone(carro.carro_usuario.precio_total)
      
      
    def test_valid_limpiar_carro_vacio(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Confirmar que el carrito está vacío inicialmente
        self.assertFalse(carro.reserva_existente())
        self.assertIsNone(carro.carro_usuario.vivienda)
        self.assertIsNone(carro.carro_usuario.fecha_inicio)
        self.assertIsNone(carro.carro_usuario.fecha_fin)
        self.assertIsNone(carro.carro_usuario.precio_total)

        # Intentar limpiar el carrito vacío
        carro.limpiar_carro()

        # Confirmar que el carrito sigue vacío y no se generaron errores
        self.assertFalse(carro.reserva_existente())
        self.assertIsNone(carro.carro_usuario.vivienda)
        self.assertIsNone(carro.carro_usuario.fecha_inicio)
        self.assertIsNone(carro.carro_usuario.fecha_fin)
        self.assertIsNone(carro.carro_usuario.precio_total)
       
        
 






