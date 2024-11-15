from django.contrib import admin
from .models import Vivienda

class ViviendaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('nombre', 'propietario')

admin.site.register(Vivienda, ViviendaAdmin)
