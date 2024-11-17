from django.shortcuts import render, redirect
from .carro import Carro
from catalogoViviendas.models import Vivienda
from catalogoViviendas.forms import ReservaForm

def reservar_vivienda(request, vivienda_id):
    carro = Carro(request)
    vivienda = Vivienda.objects.get(id=vivienda_id)
    carro.agregar(vivienda)
    return redirect('carro:detalle')

def eliminar_reserva(request):
    carro = Carro(request)
    carro.eliminar()
    return redirect('carro:detalle')

def detalle_carro(request):
    carro = Carro(request)
    return render(request, 'carro/detalle.html', {'carro': carro})

from django.shortcuts import render
from carro.carro import Carro

def detalle_carro(request):
    carro = Carro(request)
    return render(request, 'carro/detalle.html', {'carro': carro})

