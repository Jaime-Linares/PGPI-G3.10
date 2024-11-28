from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .carro import Carro
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
@login_required
def detalle_carro(request):
    carro = Carro(request)
    reserva = carro.obtener_reserva()
    return render(request, 'carro/detalle.html', {'reserva': reserva})

@require_http_methods(["POST"])
@login_required
def eliminar_reserva_carro(request):
    carro = Carro(request)
    carro.limpiar_carro()
    return redirect('carro:detalle')

 