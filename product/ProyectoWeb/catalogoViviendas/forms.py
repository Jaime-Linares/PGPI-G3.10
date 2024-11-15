from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

from .models import Vivienda



class ViviendaForm(forms.ModelForm):
    class Meta:
        model = Vivienda
        fields = [
            'nombre',
            'descripcion',
            'ubicacion',
            'imagen',
            'precio_por_dia',
            'wifi',
            'piscina',
            'parking',
            'aire_acondicionado',
            'barbacoa',
            'ducha',
            'cocina'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

