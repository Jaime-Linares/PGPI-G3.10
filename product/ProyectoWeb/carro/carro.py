from .models import Carro as CarroModel


class Carro:
    def __init__(self, request):
        self.request = request
        self.usuario = request.user if request.user.is_authenticated else None
        if self.usuario:
            self.carro_usuario, _ = CarroModel.objects.get_or_create(usuario=self.usuario)

    def agregar_reserva(self, vivienda, fecha_inicio, fecha_fin, precio_total):
        self.carro_usuario.vivienda = vivienda
        self.carro_usuario.fecha_inicio = fecha_inicio
        self.carro_usuario.fecha_fin = fecha_fin
        self.carro_usuario.precio_total = precio_total
        self.carro_usuario.save()

    def reserva_existente(self):
        return self.carro_usuario.vivienda is not None

    def obtener_reserva(self):
        if self.reserva_existente():
            return {
                "vivienda": self.carro_usuario.vivienda,
                "fecha_inicio": self.carro_usuario.fecha_inicio,
                "fecha_fin": self.carro_usuario.fecha_fin,
                "precio_total": self.carro_usuario.precio_total
            }
        return None

    def limpiar_carro(self):
        self.carro_usuario.limpiar_carro()
