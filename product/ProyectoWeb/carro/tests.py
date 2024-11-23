from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from catalogoViviendas.models import Vivienda
from carro.carro import Carro
from carro.models import Carro as CarroModel
from django.core.files.uploadedfile import SimpleUploadedFile


class CarroClassTests(TestCase):
    def setUp(self):
        # Crear un usuario para los tests
        self.usuario = User.objects.create_user(username="usuario", password="12345")
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

    def test_agregar_reserva(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Agregar una reserva
        carro.agregar_reserva(self.vivienda, "2024-01-01", "2024-01-10", 900)

        # Verificar los valores de la reserva
        self.assertEqual(carro.carro.vivienda, self.vivienda)
        self.assertEqual(str(carro.carro.fecha_inicio), "2024-01-01")
        self.assertEqual(str(carro.carro.fecha_fin), "2024-01-10")
        self.assertEqual(carro.carro.precio_total, 900)

    def test_reserva_existente(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Sin reservas
        self.assertFalse(carro.reserva_existente())

        # Agregar una reserva
        carro.agregar_reserva(self.vivienda, "2024-01-01", "2024-01-10", 900)
        self.assertTrue(carro.reserva_existente())

    def test_obtener_reserva(self):
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
        self.assertEqual(reserva["fecha_inicio"], carro.carro.fecha_inicio)
        self.assertEqual(reserva["fecha_fin"], carro.carro.fecha_fin)
        self.assertEqual(reserva["precio_total"], carro.carro.precio_total)

    def test_limpiar_carro(self):
        # Crear una instancia de Carro
        request = self.factory.get("/")
        request.user = self.usuario
        carro = Carro(request)

        # Agregar una reserva
        carro.agregar_reserva(self.vivienda, "2024-01-01", "2024-01-10", 900)

        # Limpiar el carro
        carro.limpiar_carro()

        # Verificar que los valores fueron eliminados
        self.assertIsNone(carro.carro.vivienda)
        self.assertIsNone(carro.carro.fecha_inicio)
        self.assertIsNone(carro.carro.fecha_fin)
        self.assertIsNone(carro.carro.precio_total)
