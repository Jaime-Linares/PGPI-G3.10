from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True) # Auto_now_add actualiza la fecha de creación automáticamente a la fecha actual
    updated = models.DateTimeField(auto_now_add=True) 

    # Clase Meta para configurar el nombre de la tabla en la base de datos
    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre
    
class Post(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='blog',null=True,blank=True) # Para que Django sepa donde guardar las imágenes (hay que añadir que busque en media en settings.py)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria)
    created = models.DateTimeField(auto_now_add=True) # Auto_now_add actualiza la fecha de creación automáticamente a la fecha actual
    updated = models.DateTimeField(auto_now_add=True) 

    # Clase Meta para configurar el nombre de la tabla en la base de datos
    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.titulo