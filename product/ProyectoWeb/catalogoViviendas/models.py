from django.db import models
from django.contrib.auth.models import User

class Vivienda(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viviendas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='viviendas')
    disponibilidad = models.BooleanField(default=True)
    fecha_disponible_desde = models.DateField()
    fecha_disponible_hasta = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'vivienda'
        verbose_name_plural = 'viviendas'

    def __str__(self):
        return self.nombre
