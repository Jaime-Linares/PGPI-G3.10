from django.contrib import admin
from .models import Vivienda
from .models import Reserva

class ViviendaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('nombre', 'propietario')


class ReservasAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'precio_total', 'creada', 'vivienda', 'usuario')

admin.site.register(Vivienda, ViviendaAdmin)
admin.site.register(Reserva, ReservasAdmin)
