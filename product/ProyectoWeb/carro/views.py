from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .carro import Carro


@login_required
def detalle_carro(request):
    carro = Carro(request)
    print(carro.carro)
    return render(request, 'carro/detalle.html', {'carro': carro})


@login_required
def eliminar_reserva(request):
    carro = Carro(request)
    carro.limpiar_carro()
    messages.success(request, "Reserva eliminada del carrito.")
    return redirect('carro:detalle')

 