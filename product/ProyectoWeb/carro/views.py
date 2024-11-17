from django.shortcuts import render, redirect
from .carro import Carro

def eliminar_reserva(request):
    carro = Carro(request)
    carro.eliminar()
    return redirect('carro:detalle')

def detalle_carro(request):
    carro = Carro(request)
    return render(request, 'carro/detalle.html', {'carro': carro})


