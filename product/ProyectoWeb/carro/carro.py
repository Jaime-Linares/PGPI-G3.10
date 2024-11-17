import json
from datetime import timedelta
from django.utils import timezone

class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user_id = str(request.user.id) if request.user.is_authenticated else 'anon'
        self.carro_key = f"carro_{self.user_id}"
        self.carro = self._cargar_carro()

    def _cargar_carro(self):
        # Cargar el carrito desde una cookie si existe
        carro_cookie = self.request.COOKIES.get(self.carro_key)
        if carro_cookie:
            try:
                return json.loads(carro_cookie)
            except json.JSONDecodeError:
                return {}
        return {}

    def guardar_carro(self, response):
        # Guardar el carrito en una cookie utilizando solo `max_age`
        response.set_cookie(
            self.carro_key,
            json.dumps(self.carro),
            max_age=60 * 60 * 24 * 7,  # Una semana en segundos
            httponly=True
        )


    def agregar_reserva(self, vivienda, fecha_inicio, fecha_fin, precio_total):
        self.carro["reserva"] = {
            "vivienda_id": vivienda.id,
            "nombre": vivienda.nombre,
            "precio_por_dia": str(vivienda.precio_por_dia),
            "precio_total": str(precio_total),
            "imagen": vivienda.imagen.url,
            "fecha_inicio": fecha_inicio.strftime('%d-%m-%Y'),
            "fecha_fin": fecha_fin.strftime('%d-%m-%Y')
        }

    def reserva_existente(self):
        return "reserva" in self.carro

    def obtener_reserva(self):
        return self.carro.get("reserva", None)

    def limpiar_carro(self, response):
        response.delete_cookie(self.carro_key)
