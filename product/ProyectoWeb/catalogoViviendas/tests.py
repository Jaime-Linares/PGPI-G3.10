from django.test import TestCase
from django.contrib.auth.models import Group, User
from catalogoViviendas.models import Vivienda, Reserva
from catalogoViviendas.views import validar_reserva
from django.utils import timezone
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

class ViviendaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="testuser", password="testpassword123")
        self.cliente = User.objects.create_user(username="cliente", password="password123")
        cliente_group, _ = Group.objects.get_or_create(name="Cliente")
        self.cliente.groups.add(cliente_group)

        self.vivienda = Vivienda.objects.create(
            propietario=self.usuario,
            nombre="Casa Test",
            descripcion="Casa para pruebas",
            ubicacion="Calle Falsa",
            precio_por_dia=100.00,
            imagen=SimpleUploadedFile(name='viviendas/el_molino.jpg', content=b'', content_type='image/jpeg')
        )

        self.reserva = Reserva.objects.create(
            vivienda=self.vivienda,
            usuario=self.cliente,
            fecha_inicio=timezone.now().date() + timezone.timedelta(days=10),
            fecha_fin=timezone.now().date() + timezone.timedelta(days=15),
            precio_total=500.00
        )
      
    def test_invalid_propietario_intenta_validar_reserva(self):
        # Asegurar que el usuario actual es un propietario
        propietario_group, _ = Group.objects.get_or_create(name="Propietario")
        self.usuario.groups.add(propietario_group)

        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Intentar validar una reserva como propietario
        today = timezone.now().date()
        fecha_inicio = today + timezone.timedelta(days=20)
        fecha_fin = today + timezone.timedelta(days=25)

        # Llamar al método de validación
        error = validar_reserva(self.vivienda, fecha_inicio, fecha_fin)

        # Verificar que no hay restricciones adicionales solo por ser propietario
        self.assertIsNone(error)

    def test_invalid_validar_reserva_fecha_fin_anterior_a_inicio(self):
        today = timezone.now().date()
        fecha_inicio = today + timezone.timedelta(days=10)
        fecha_fin = today + timezone.timedelta(days=5)
        error = validar_reserva(self.vivienda, fecha_inicio, fecha_fin)
        self.assertEqual(error, "La fecha de fin debe ser posterior a la fecha de inicio.")


    def test_invalid_validar_reserva_fecha_inicio_en_el_pasado(self):
        today = timezone.now().date()
        fecha_inicio = today - timezone.timedelta(days=1)
        fecha_fin = today + timezone.timedelta(days=5)
        error = validar_reserva(self.vivienda, fecha_inicio, fecha_fin)
        self.assertEqual(error, "No se puede realizar una reserva en fechas pasadas.")


    def test_invalid_validar_reserva_fecha_fin_en_el_pasado(self):
        today = timezone.now().date()
        fecha_inicio = today - timezone.timedelta(days=5)
        fecha_fin = today - timezone.timedelta(days=1)
        error = validar_reserva(self.vivienda, fecha_inicio, fecha_fin)
        self.assertEqual(error, "No se puede realizar una reserva en fechas pasadas.")


    def test_invalid_validar_reserva_fechas_superpuestas_con_reserva_existente(self):
        today = timezone.now().date()
        fecha_inicio = today + timezone.timedelta(days=12)  # Dentro de la reserva existente
        fecha_fin = today + timezone.timedelta(days=14)
        error = validar_reserva(self.vivienda, fecha_inicio, fecha_fin)
        self.assertEqual(error, "Algunas fechas seleccionadas ya están reservadas para esta vivienda.")


    def test_reserva_valida(self):
        today = timezone.now().date()
        fecha_inicio = today + timezone.timedelta(days=16)  # Fuera del rango de reservas existentes
        fecha_fin = today + timezone.timedelta(days=20)
        error = validar_reserva(self.vivienda, fecha_inicio, fecha_fin)
        self.assertIsNone(error)
        
        
    def test_invalid_cliente_no_puede_crear_vivienda(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Intentar crear una vivienda
        response = self.client.post(reverse('catalogoViviendas:crear_vivienda'), {
            "nombre": "Vivienda Cliente",
            "descripcion": "Descripción de prueba",
            "ubicacion": "Dirección del cliente",
            "precio_por_dia": 100.00,
        })

        # Verificar que no se permite la creación
        self.assertEqual(response.status_code, 302)  # Redirige al Home
        self.assertRedirects(response, reverse('Home'))  # Confirma la redirección
        self.assertEqual(Vivienda.objects.filter(nombre="Vivienda Cliente").count(), 0)  # No se creó la vivienda
        
    
    def test_invalid_cliente_no_puede_acceder_catalogo_viviendas_propietario(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Intentar acceder al catálogo de viviendas del propietario
        response = self.client.get(reverse('catalogoViviendas:catalogo_viviendas_propietario'))

        # Verificar que el cliente es redirigido al Home (no tiene permisos)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Home'))
        
        
    def test_valid_eliminar_reserva_cliente(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Generar la URL para eliminar la reserva
        url = reverse('catalogoViviendas:eliminar_reserva', args=[self.reserva.id])

        # Enviar solicitud para eliminar la reserva
        response = self.client.post(url, follow=True)

        # Verificar que la reserva fue eliminada
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reserva.objects.filter(id=self.reserva.id).count(), 0)
        
    
    def test_invalid_cliente_no_puede_eliminar_reserva_por_restricciones_menos_7_dias(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Crear una reserva que no cumple las condiciones para ser eliminada
        fecha_inicio = timezone.now().date() + timezone.timedelta(days=5)  # Menos de 7 días en el futuro
        self.reserva = Reserva.objects.create(
            vivienda=self.vivienda,
            usuario=self.cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_inicio + timezone.timedelta(days=2),
            precio_total=200.00
        )

        # Generar la URL para intentar eliminar la reserva
        url = reverse('catalogoViviendas:eliminar_reserva', args=[self.reserva.id])

        # Enviar solicitud para eliminar la reserva
        response = self.client.post(url, follow=True)

        # Verificar que la reserva no fue eliminada y que el usuario recibió un mensaje de error
        self.assertEqual(response.status_code, 200)  # Redirige a la página correspondiente
        self.assertContains(response, "No puedes cancelar esta reserva.")  # Mensaje esperado
        self.assertEqual(Reserva.objects.filter(id=self.reserva.id).count(), 1)  # La reserva aún existe


    def test_invalid_cliente_no_puede_eliminar_reserva_en_curso(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Crear una reserva cuya fecha de inicio es hoy (ya está en curso)
        fecha_inicio = timezone.now().date()  # Fecha actual
        self.reserva = Reserva.objects.create(
            vivienda=self.vivienda,
            usuario=self.cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_inicio + timezone.timedelta(days=2),
            precio_total=300.00
        )

        # Generar la URL para intentar eliminar la reserva
        url = reverse('catalogoViviendas:eliminar_reserva', args=[self.reserva.id])

        # Enviar solicitud para eliminar la reserva
        response = self.client.post(url, follow=True)

        # Verificar que la reserva no fue eliminada y que el usuario recibió un mensaje de error
        self.assertEqual(response.status_code, 200)  # La redirección ocurre correctamente
        self.assertContains(response, "No puedes cancelar esta reserva.")  # Mensaje esperado
        self.assertEqual(Reserva.objects.filter(id=self.reserva.id).count(), 1)  # La reserva sigue en la base de datos


    def test_invalid_propietario_no_puede_eliminar_reserva(self):
        # Asegurar que el usuario propietario pertenece al grupo "Propietario"
        propietario_group, _ = Group.objects.get_or_create(name="Propietario")
        self.usuario.groups.add(propietario_group)

        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Generar la URL para intentar eliminar una reserva
        url = reverse('catalogoViviendas:eliminar_reserva', args=[self.reserva.id])

        # Enviar solicitud para eliminar la reserva
        response = self.client.post(url, follow=True)

        # Verificar que la reserva no fue eliminada
        self.assertEqual(response.status_code, 404)  # Código de respuesta esperado para acceso prohibido
        self.assertEqual(Reserva.objects.filter(id=self.reserva.id).count(), 1)  # La reserva aún existe


    def test_valid_cliente_puede_acceder_historial_reservas(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Crear dos reservas adicionales para el cliente: una que puede eliminarse y otra que no
        today = timezone.now().date()
        Reserva.objects.create(
            vivienda=self.vivienda,
            usuario=self.cliente,
            fecha_inicio=today + timezone.timedelta(days=10),  # Puede eliminarse
            fecha_fin=today + timezone.timedelta(days=12),
            precio_total=200.00
        )
        Reserva.objects.create(
            vivienda=self.vivienda,
            usuario=self.cliente,
            fecha_inicio=today + timezone.timedelta(days=5),  # No puede eliminarse
            fecha_fin=today + timezone.timedelta(days=7),
            precio_total=150.00
        )

        # Generar la URL para acceder al historial de reservas
        url = reverse('catalogoViviendas:historial_reservas')

        # Enviar solicitud para acceder al historial de reservas
        response = self.client.get(url)

        # Verificar que el acceso fue exitoso
        self.assertEqual(response.status_code, 200)

        # Verificar que el template correcto fue renderizado
        self.assertTemplateUsed(response, "catalogoViviendas/cliente/historial_reservas.html")

        # Verificar que las reservas aparecen en el contexto
        self.assertIn('reservas', response.context)
        reservas = response.context['reservas']
        self.assertEqual(len(reservas), 3)  # Tres reservas: una del setup y dos creadas aquí

        
    
    def test_invalid_propietario_no_puede_acceder_historial_reservas(self):
        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Generar la URL para acceder al historial de reservas
        url = reverse('catalogoViviendas:historial_reservas')

        # Enviar solicitud para acceder al historial de reservas
        response = self.client.get(url)

        # Verificar que el propietario es redirigido al Home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Home'))

        # Verificar que el contenido no contiene elementos del historial de reservas
        follow_response = self.client.get(response.url)  # Seguir la redirección
        self.assertNotContains(follow_response, "historial_reservas.html")


        
    def test_invalid_crear_vivienda_sin_descripcion(self):
        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Intentar crear una vivienda sin el campo "descripcion"
        response = self.client.post(reverse('catalogoViviendas:crear_vivienda'), {
            "nombre": "Nueva Vivienda",
            "descripcion": "",
            "ubicacion": "Dirección de prueba",
            "precio_por_dia": 150.00,
            "propietario": self.usuario.id,
        })

        # Verificar que la vista redirige tras fallo de validación (302)
        self.assertEqual(response.status_code, 302)

        # Verificar que la vivienda no se creó en la base de datos
        self.assertEqual(Vivienda.objects.filter(nombre="Nueva Vivienda").count(), 0)

    
    def test_invalid_crear_vivienda_sin_nombre(self):
        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Intentar crear una vivienda sin el campo "nombre"
        response = self.client.post(reverse('catalogoViviendas:crear_vivienda'), {
            "nombre": "",
            "descripcion": "Descripción de prueba",
            "ubicacion": "Dirección de prueba",
            "precio_por_dia": 150.00,
            "propietario": self.usuario.id,
        })

        # Verificar que la vista redirige tras fallo de validación (302)
        self.assertEqual(response.status_code, 302)

        # Verificar que la vivienda no se creó en la base de datos
        self.assertEqual(Vivienda.objects.filter(descripcion="Descripción de prueba").count(), 0)
        
        
    def test_invalid_crear_vivienda_sin_ubicacion(self):
        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Intentar crear una vivienda sin el campo "ubicacion"
        response = self.client.post(reverse('catalogoViviendas:crear_vivienda'), {
            "nombre": "Nueva Vivienda",
            "descripcion": "Descripción de prueba",
            "ubicacion": "",
            "precio_por_dia": 150.00,
            "propietario": self.usuario.id,
        })

        # Verificar que la vista redirige tras fallo de validación (302)
        self.assertEqual(response.status_code, 302)

        # Verificar que la vivienda no se creó en la base de datos
        self.assertEqual(Vivienda.objects.filter(nombre="Nueva Vivienda").count(), 0)
     
        
    def test_invalid_crear_vivienda_sin_precio(self):
        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Intentar crear una vivienda sin el campo "precio_por_dia"
        response = self.client.post(reverse('catalogoViviendas:crear_vivienda'), {
            "nombre": "Vivienda Sin Precio",
            "descripcion": "Descripción de prueba",
            "ubicacion": "Dirección de prueba",
            "precio_por_dia": "",
        })

        # Verificar que la vista redirige tras fallo de validación (302)
        self.assertEqual(response.status_code, 302)

        # Verificar que la vivienda no se creó en la base de datos
        self.assertEqual(Vivienda.objects.filter(nombre="Vivienda Sin Precio").count(), 0)
    
    
    def crear_imagen_valida(self):
        # Crear una imagen en memoria
        imagen = BytesIO()
        img = Image.new('RGB', (100, 100), color='red')  # Crear una imagen roja de 100x100 píxeles
        img.save(imagen, format='JPEG')
        imagen.seek(0)  # Volver al inicio del archivo en memoria
        return SimpleUploadedFile('test_image.jpg', imagen.read(), content_type='image/jpeg')
    

    def test_valid_crear_vivienda(self):
        # Asegurar que el usuario pertenece al grupo "Propietario"
        propietario_group, _ = Group.objects.get_or_create(name="Propietario")
        self.usuario.groups.add(propietario_group)

        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Generar una imagen válida para el test
        imagen = self.crear_imagen_valida()

        # Crear una vivienda con los campos requeridos
        response = self.client.post(reverse('catalogoViviendas:crear_vivienda'), {
            "nombre": "Vivienda Básica",
            "descripcion": "Descripción básica de la vivienda.",
            "ubicacion": "Ubicación básica",
            "precio_por_dia": 100.00,
            "imagen": imagen,
        }, follow=True)

        # Verificar que la respuesta es exitosa
        self.assertEqual(response.status_code, 200)

        # Verificar que la vivienda fue creada correctamente
        vivienda = Vivienda.objects.filter(nombre="Vivienda Básica").first()
        self.assertIsNotNone(vivienda)  # Verifica que la vivienda existe
        self.assertEqual(vivienda.descripcion, "Descripción básica de la vivienda.")
        self.assertEqual(vivienda.ubicacion, "Ubicación básica")
        self.assertEqual(vivienda.precio_por_dia, 100.00)
        self.assertIsNotNone(vivienda.imagen)  # Verifica que la imagen fue guardada


    def test_valid_eliminar_vivienda(self):
        # Asegurar que el usuario pertenece al grupo "Propietario"
        propietario_group, _ = Group.objects.get_or_create(name="Propietario")
        self.usuario.groups.add(propietario_group)

        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Verificar que la vivienda existe antes de eliminarla
        vivienda_id = self.vivienda.id
        self.assertEqual(Vivienda.objects.filter(id=vivienda_id).count(), 1)

        # Enviar solicitud para eliminar la vivienda
        response = self.client.post(reverse('catalogoViviendas:eliminar_vivienda', args=[vivienda_id]), follow=True)

        # Verificar que la solicitud fue exitosa
        self.assertEqual(response.status_code, 200)

        # Verificar que la vivienda fue eliminada
        self.assertEqual(Vivienda.objects.filter(id=vivienda_id).count(), 0)
        
    
    def test_valid_acceso_catalogo_viviendas_propietario(self):
        # Asegurar que el usuario pertenece al grupo "Propietario"
        propietario_group, _ = Group.objects.get_or_create(name="Propietario")
        self.usuario.groups.add(propietario_group)

        # Iniciar sesión como propietario
        self.client.login(username="testuser", password="testpassword123")

        # Acceder al catálogo de viviendas del propietario
        response = self.client.get(reverse('catalogoViviendas:catalogo_viviendas_propietario'))

        # Verificar que el acceso fue exitoso
        self.assertEqual(response.status_code, 200)

        # Verificar que el template correcto fue renderizado
        self.assertTemplateUsed(response, "catalogoViviendas/propietario/catalogo_viviendas_propietario.html")

        # Verificar que las viviendas del propietario aparecen en el contexto
        self.assertIn('viviendas', response.context)
        self.assertTrue(response.context['es_propietario'])
        viviendas = response.context['viviendas']
        self.assertEqual(len(viviendas), 1)  # Solo una vivienda creada en setup
        self.assertEqual(viviendas[0], self.vivienda)  # Verificar que es la vivienda del propietario
       
        
    def test_cliente_puede_acceder_catalogo_sin_filtros(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Acceder al catálogo sin filtros
        url = reverse('catalogoViviendas:catalogo_viviendas')
        response = self.client.get(url)

        # Verificar que el acceso fue exitoso
        self.assertEqual(response.status_code, 200)

        # Verificar que el template correcto fue renderizado
        self.assertTemplateUsed(response, "catalogoViviendas/cliente/catalogo_viviendas_cliente.html")

        # Verificar que las viviendas están en el contexto
        self.assertIn('viviendas', response.context)
        viviendas = response.context['viviendas']
        
        # Asegúrate de que las viviendas incluyan las esperadas
        self.assertTrue(self.vivienda in viviendas)

        
        
    def test_cliente_filtra_catalogo_por_nombre(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Acceder al catálogo con filtro de nombre
        url = reverse('catalogoViviendas:catalogo_viviendas') + '?q=Casa'
        response = self.client.get(url)

        # Verificar que el acceso fue exitoso
        self.assertEqual(response.status_code, 200)

        # Verificar que las viviendas filtradas están en el contexto
        self.assertIn('viviendas', response.context)
        viviendas = response.context['viviendas']
        
        # Verificar que solo aparecen las viviendas con el nombre filtrado
        self.assertTrue(all("Casa" in vivienda.nombre for vivienda in viviendas))
        self.assertTrue(self.vivienda in viviendas)



    def test_cliente_filtra_catalogo_por_ubicacion(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Acceder al catálogo con filtro de ubicación
        url = reverse('catalogoViviendas:catalogo_viviendas') + '?ubicacion=Calle'
        response = self.client.get(url)

        # Verificar que el acceso fue exitoso
        self.assertEqual(response.status_code, 200)

        # Verificar que las viviendas filtradas están en el contexto
        self.assertIn('viviendas', response.context)
        viviendas = response.context['viviendas']
        self.assertEqual(len(viviendas), 1)  # La vivienda coincide con el filtro
        self.assertEqual(viviendas[0], self.vivienda)
        
        
    def test_cliente_filtra_catalogo_por_nombre_y_ubicacion(self):
        # Iniciar sesión como cliente
        self.client.login(username="cliente", password="password123")

        # Acceder al catálogo con filtro de nombre y ubicación
        url = reverse('catalogoViviendas:catalogo_viviendas') + '?q=Casa&ubicacion=Calle'
        response = self.client.get(url)

        # Verificar que el acceso fue exitoso
        self.assertEqual(response.status_code, 200)

        # Verificar que las viviendas filtradas están en el contexto
        self.assertIn('viviendas', response.context)
        viviendas = response.context['viviendas']
        self.assertEqual(len(viviendas), 1)  # La vivienda coincide con ambos filtros
        self.assertEqual(viviendas[0], self.vivienda)


