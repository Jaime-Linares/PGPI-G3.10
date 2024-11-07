from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Añadimos una columna personalizada para mostrar el grupo (rol)
    list_display = ('username', 'email', 'get_group', 'is_staff', 'is_active')

    def get_group(self, obj):
        # Muestra el primer grupo al que pertenece el usuario
        return ", ".join([group.name for group in obj.groups.all()])

    get_group.short_description = 'Rol'  # Título de la columna

# Registramos el UserAdmin personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
