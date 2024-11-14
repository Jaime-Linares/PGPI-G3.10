from django.db import models
from django.contrib.auth.models import User



class Vivienda(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viviendas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=100)
    wifi = models.BooleanField(default=False)
    piscina = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    aire_acondicionado = models.BooleanField(default=False)
    barbacoa = models.BooleanField(default=False)
    ducha = models.BooleanField(default=False)
    cocina = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='viviendas',blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    precio_por_dia = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'vivienda'
        verbose_name_plural = 'viviendas'

    def __str__(self):
        return self.nombre
    

class Reserva(models.Model):
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.vivienda.nombre}"