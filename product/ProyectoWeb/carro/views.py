from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .carro import Carro


@login_required
def detalle_carro(request):
    carro = Carro(request)
    reserva = carro.obtener_reserva()
    return render(request, 'carro/detalle.html', {'reserva': reserva})


@login_required
def eliminar_reserva_carro(request):
    carro = Carro(request)
    carro.limpiar_carro()
    messages.success(request, "Reserva eliminada del carrito.")
    return redirect('carro:detalle')

 