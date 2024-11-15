from django import forms
from .models import Reserva, Vivienda



class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


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
        for field_name, field in self.fields.items():
            if field_name not in ['wifi', 'piscina', 'parking', 'aire_acondicionado', 'barbacoa', 'ducha', 'cocina']:
                field.required = True
            field.widget.attrs.update({'class': 'form-control'})
        

