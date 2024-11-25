# from django.test import TestCase, Client
# from django.contrib.auth.models import User
# from unittest.mock import patch, MagicMock
# from carro.models import Carro
# from django.urls import reverse
# from catalogoViviendas.models import Reserva, Vivienda


# class PagoTests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")
#         self.client.login(username="testuser", password="testpassword123")

#         # Ajustar los campos del modelo Vivienda, incluyendo precio_por_dia
#         self.vivienda = Vivienda.objects.create(
#             nombre="Test Vivienda",
#             descripcion="Test Descripción",
#             ubicacion="Test Ubicación",
#             precio_por_dia=100  # Campo obligatorio
#         )
#         self.carro = Carro.objects.create(
#             usuario=self.user,
#             vivienda=self.vivienda,
#             fecha_inicio="2024-11-01",
#             fecha_fin="2024-11-07",
#             precio_total=600,
#         )

#     @patch("braintree.Transaction.sale")
#     def test_confirmar_reserva_successful_payment(self, mock_braintree_sale):
#         # Mock a successful Braintree transaction
#         mock_braintree_sale.return_value.is_success = True
#         mock_braintree_sale.return_value.transaction = MagicMock(id="fake_transaction_id")

#         data = {"payment_method_nonce": "fake_nonce"}
#         response = self.client.post(reverse("pago:confirmar_reserva"), data)

#         # Verificar redirección y reserva creada
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "pago/reserva_exitosa.html")
#         self.assertTrue(Reserva.objects.filter(usuario=self.user, vivienda=self.vivienda).exists())

#         # Verificar que el carro está vacío después del pago
#         self.carro.refresh_from_db()
#         self.assertIsNone(self.carro.vivienda)

#     @patch("braintree.Transaction.sale")
#     def test_confirmar_reserva_failed_payment(self, mock_braintree_sale):
#         # Mock a failed Braintree transaction
#         mock_braintree_sale.return_value.is_success = False
#         mock_braintree_sale.return_value.message = "Payment failed"

#         data = {"payment_method_nonce": "fake_nonce"}
#         response = self.client.post(reverse("pago:confirmar_reserva"), data)

#         # Verificar redirección y mensaje de error
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("carro:detalle"))
#         self.assertContains(response, "Error al procesar el pago: Payment failed")

#     def test_confirmar_reserva_no_carro(self):
#         # Eliminar el carro para simular el error
#         self.carro.delete()

#         data = {"payment_method_nonce": "fake_nonce"}
#         response = self.client.post(reverse("pago:confirmar_reserva"), data)

#         # Verificar redirección y mensaje de error
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("carro:detalle"))
#         self.assertContains(response, "El monto debe ser mayor que cero.")
