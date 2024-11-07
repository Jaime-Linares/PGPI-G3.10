from django.db import models

# Create your models here.

class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    contenido = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='servicios') # Para que Django sepa donde guardar las imágenes (hay que añadir que busque en media en settings.py)
    created = models.DateTimeField(auto_now_add=True) # Auto_now_add actualiza la fecha de creación automáticamente a la fecha actual
    updated = models.DateTimeField(auto_now_add=True) 

    # Clase Meta para configurar el nombre de la tabla en la base de datos
    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'

    def __str__(self):
        return self.nombre