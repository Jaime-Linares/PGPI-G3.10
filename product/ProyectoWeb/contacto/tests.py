from django.test import TestCase
from django.urls import reverse
from django.core import mail

class ContactoViewsTests(TestCase):
    def test_renderizar_formulario_contacto(self):
        response = self.client.get(reverse("Contacto"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacto/contacto.html")
        self.assertContains(response, "<form")

    def test_envio_formulario_contacto_valido(self):
        datos_formulario = {
            "nombre": "Test User",
            "email": "testuser@example.com",
            "contenido": "Este es un mensaje de prueba.",
        }
        response = self.client.post(reverse("Contacto"), data=datos_formulario)
        self.assertRedirects(response, "/contacto/?valido")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Test User", mail.outbox[0].body)
        self.assertIn("Este es un mensaje de prueba.", mail.outbox[0].body)