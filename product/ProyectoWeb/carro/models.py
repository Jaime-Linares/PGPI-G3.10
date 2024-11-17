from django.db import models
from django.contrib.auth.models import User
from catalogoViviendas.models import Vivienda


class Carro(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carro')
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Carro de {self.usuario.username}"

    def limpiar_carro(self):
        self.vivienda = None
        self.fecha_inicio = None
        self.fecha_fin = None
        self.precio_total = None
        self.save()
