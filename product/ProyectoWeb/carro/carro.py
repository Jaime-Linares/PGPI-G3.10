class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {}
        self.carro = carro

    def agregar_reserva(self, vivienda, fecha_inicio, fecha_fin, precio_total):
        self.carro.clear()  # Limpiar el carrito antes de añadir una nueva reserva
        self.carro["reserva"] = {
            "vivienda_id": vivienda.id,
            "nombre": vivienda.nombre,
            "precio_por_dia": str(vivienda.precio_por_dia),
            "precio_total": str(precio_total),
            "imagen": vivienda.imagen.url,
            "fecha_inicio": fecha_inicio.strftime('%d-%m-%Y'),
            "fecha_fin": fecha_fin.strftime('%d-%m-%Y')
        }
        self.guardar_carro()

    def reserva_existente(self):
        return "reserva" in self.carro

    def eliminar(self):
        if "reserva" in self.carro:
            del self.carro["reserva"]
        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True
