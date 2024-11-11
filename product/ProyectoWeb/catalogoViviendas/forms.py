from django import forms
from .models import Vivienda



class ViviendaForm(forms.ModelForm):
    class Meta:
        model = Vivienda
        fields = [
            'nombre',
            'descripcion',
            'ubicacion',
            'imagen',
            'disponibilidad',
            'fecha_disponible_desde',
            'fecha_disponible_hasta',
            'precio_por_dia'
        ]
        widgets = {
            'fecha_disponible_desde': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'fecha_disponible_hasta': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.fecha_disponible_desde:
                self.fields['fecha_disponible_desde'].widget.attrs['value'] = self.instance.fecha_disponible_desde.strftime('%Y-%m-%d')
            if self.instance.fecha_disponible_hasta:
                self.fields['fecha_disponible_hasta'].widget.attrs['value'] = self.instance.fecha_disponible_hasta.strftime('%Y-%m-%d')

