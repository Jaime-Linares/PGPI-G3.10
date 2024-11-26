from django.test import TestCase, Client
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from carro.models import Carro
from django.urls import reverse
from catalogoViviendas.models import Reserva, Vivienda
from django.core.files.uploadedfile import SimpleUploadedFile


class PagoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")
        self.client.login(username="testuser", password="testpassword123")

        self.image = SimpleUploadedFile(
            "test_image.jpg", 
            content=b"file_content", 
            content_type="image/jpeg"
        )
    # Crear una instancia de Vivienda con un propietario
        self.vivienda = Vivienda.objects.create(
            nombre="Test Vivienda",
            descripcion="Test Descripción",
            ubicacion="Test Ubicación",
            precio_por_dia=100,  # Campo obligatorio
            propietario=self.user , # Asignar propietario
            imagen=self.image
        )

    # Crear un Carro asociado al usuario y la vivienda
        self.carro = Carro.objects.create(
            usuario=self.user,
            vivienda=self.vivienda,
            fecha_inicio="2024-11-01",
            fecha_fin="2024-11-07",
            precio_total=600,
    )

 
    @patch("braintree.Transaction.sale")
    def test_confirmar_reserva_successful_payment(self, mock_braintree_sale):
        # Simular una transacción exitosa de Braintree
        mock_braintree_sale.return_value.is_success = True
        mock_braintree_sale.return_value.transaction = MagicMock(id="fake_transaction_id")

        data = {"payment_method_nonce": "fake_nonce"}
        response = self.client.post(reverse("pago:confirmar_reserva"), data)

        # Verificar que la respuesta sea exitosa y se use la plantilla correcta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pago/reserva_exitosa.html")
        self.assertTrue(Reserva.objects.filter(usuario=self.user, vivienda=self.vivienda).exists())

        # Verificar que el carro esté vacío después del pago
        self.carro.refresh_from_db()
        self.assertIsNone(self.carro.vivienda)

    @patch("braintree.Transaction.sale")
    def test_confirmar_reserva_failed_payment(self, mock_braintree_sale):
        # Simular una transacción fallida de Braintree
        mock_braintree_sale.return_value.is_success = False
        mock_braintree_sale.return_value.message = "Payment failed"

        data = {"payment_method_nonce": "fake_nonce"}
        response = self.client.post(reverse("pago:confirmar_reserva"), data)

        # Verificar redirección y mensaje de error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("carro:detalle"))


    def test_confirmar_reserva_no_carro(self):
        # Eliminar el carro para simular el caso de error
        self.carro.delete()

        data = {"payment_method_nonce": "fake_nonce"}
        response = self.client.post(reverse("pago:confirmar_reserva"), data)

        # Verificar redirección y mensaje de error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("carro:detalle"))

    def test_confirmar_reserva_no_payment_method_nonce(self):
        response = self.client.post(reverse("pago:confirmar_reserva"))

        # Verificar redirección y mensaje de error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("carro:detalle"))

    def test_confirmar_reserva_no_vivienda(self):
        # Eliminar la vivienda para simular el caso de error
        self.vivienda.delete()

        data = {"payment_method_nonce": "fake_nonce"}
        response = self.client.post(reverse("pago:confirmar_reserva"), data)

        # Verificar redirección y mensaje de error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("carro:detalle"))

    def test_confirmar_reserva_no_fecha_fin(self):
        # Modificar el carro para simular el caso de error
        self.carro.fecha_fin = None
        self.carro.save()

        data = {"payment_method_nonce": "fake_nonce"}
        response = self.client.post(reverse("pago:confirmar_reserva"), data)

        # Verificar redirección y mensaje de error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("carro:detalle"))

    def test_confirmar_reserva_no_fecha_inicio(self):
        # Modificar el carro para simular el caso de error
        self.carro.fecha_inicio = None
        self.carro.save()

        data = {"payment_method_nonce": "fake_nonce"}
        response = self.client.post(reverse("pago:confirmar_reserva"), data)

        # Verificar redirección y mensaje de error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("carro:detalle"))
    
    



