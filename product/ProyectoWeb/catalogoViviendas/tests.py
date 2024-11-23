from django.test import TestCase
from django.contrib.auth.models import Group, User
from catalogoViviendas.models import Vivienda, Reserva
from django.utils import timezone
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class ViviendaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="testuser", password="testpassword123")
        self.vivienda = Vivienda.objects.create(
            propietario=self.usuario,
            nombre="Casa Test",
            descripcion="Casa para pruebas",
            ubicacion="Calle Falsa",
            precio_por_dia=100.00,
            imagen=SimpleUploadedFile(name='viviendas/el_molino.jpg', content=b'', content_type='image/jpeg')
        )

    def test_crear_vivienda(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(reverse('catalogoViviendas:crear_vivienda'), {
            "nombre": "Nueva Vivienda",
            "descripcion": "Descripción de prueba",
            "ubicacion": "Dirección de prueba",
            "precio_por_dia": 150.00,
            "propietario": self.usuario.id,
        })
        self.assertEqual(response.status_code, 302)

    # def test_eliminar_vivienda(self):
    #     self.client.login(username="propietario", password="password")  # Autenticación
    #     response = self.client.post(f'/catalogoViviendas/eliminar/{self.vivienda.id}/')
    #     self.assertEqual(response.status_code, 302)  # Redirección tras éxito
    #     self.assertEqual(Vivienda.objects.count(), 0)  # La vivienda fue eliminada


class ReservaTests(TestCase):
    def setUp(self):
        self.cliente_group, _ = Group.objects.get_or_create(name="Cliente")
        self.cliente = User.objects.create_user(username="cliente", password="password")
        self.cliente.groups.add(self.cliente_group)

        self.propietario_group, _ = Group.objects.get_or_create(name="Propietario")
        self.propietario = User.objects.create_user(username="propietario", password="password")
        self.propietario.groups.add(self.propietario_group)

        self.usuario = User.objects.create_user(username="testuser", password="testpassword123")
        self.vivienda = Vivienda.objects.create(
            propietario=self.usuario,
            nombre="Casa Test",
            descripcion="Casa para pruebas",
            ubicacion="Calle Falsa 123",
            precio_por_dia=100.00,
            imagen=SimpleUploadedFile(
                name='test_image.jpg',
                content=b'',
                content_type='image/jpeg'
            )
        )
        self.client.login(username="testuser", password="testpassword123")


    # def test_crear_reserva(self):
    #     self.client.login(username="cliente", password="password")  # Autenticación
    #     response = self.client.post(f'/catalogoViviendas/reserva/{self.vivienda.id}/', {
    #         'fecha_inicio': '2024-01-01',
    #         'fecha_fin': '2024-01-10',
    #         'usuario': self.usuario.id,
    #         'vivienda': self.vivienda.id,
    #     })
    #     self.assertEqual(Reserva.objects.count(), 1)  # Se creó una reserva

    def test_validar_reserva_fechas_invalidas(self):
        self.client.login(username="cliente", password="password")  # Autenticación
        response = self.client.post(f'/catalogoViviendas/detalle/{self.vivienda.id}/', {
            'fecha_inicio': (timezone.now() + timezone.timedelta(days=2)).date(),
            'fecha_fin': timezone.now().date(),
            'usuario': self.cliente.id,
            
        })
        self.assertEqual(response.status_code, 200)  # Cambiar a 302 si redirige
        self.assertContains(response, "La fecha de fin debe ser posterior a la fecha de inicio.")




class ViviendaViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cliente", password="password123")
        self.vivienda = Vivienda.objects.create(
            propietario=self.user,
            nombre="Casa Test",
            descripcion="Casa para pruebas",
            ubicacion="Calle Falsa 123",
            precio_por_dia=100.00
        )

    # def test_detalle_vivienda(self):
    #     self.client.login(username="cliente", password="password123")
    #     response = self.client.get(f"/catalogoViviendas/detalle/{self.vivienda.id}/")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Casa Test")