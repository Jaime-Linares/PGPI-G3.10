from django.contrib import admin
from .models import Vivienda

class ViviendaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('nombre', 'propietario', 'disponibilidad', 'fecha_disponible_desde', 'fecha_disponible_hasta')
    list_filter = ('disponibilidad',)

admin.site.register(Vivienda, ViviendaAdmin)
