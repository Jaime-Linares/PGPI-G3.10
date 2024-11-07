from django.contrib import admin
from .models import Post,Categoria

# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated')

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated')

admin.site.register(Post,PostAdmin)
admin.site.register(Categoria,CategoriaAdmin)
