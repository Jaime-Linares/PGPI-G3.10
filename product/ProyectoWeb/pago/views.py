import braintree
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from carro.carro import Carro
from catalogoViviendas.models import Reserva, Vivienda
import datetime

def generar_client_token():
    return braintree.ClientToken.generate()

from carro.models import Carro

@login_required
def confirmar_reserva(request):
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce')

        # Obtener la reserva actual del carro del usuario
        try:
            carro = Carro.objects.get(usuario=request.user)
            total = float(carro.precio_total)
        except Carro.DoesNotExist:
            total = 0

        print("Total obtenido de la base de datos:", total)

        # Verifica si el total es mayor que cero antes de intentar la transacción
        if total <= 0:
            messages.error(request, "El monto debe ser mayor que cero.")
            return redirect('carro:detalle')

        # Procesar el pago con Braintree
        result = braintree.Transaction.sale({
            "amount": f"{total:.2f}",
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        print("Resultado del pago:", result.is_success)

        if result.is_success:
            # Crear y guardar la reserva en la base de datos usando la información del carro
            Reserva.objects.create(
                vivienda=carro.vivienda,
                usuario=request.user,
                fecha_inicio=carro.fecha_inicio,
                fecha_fin=carro.fecha_fin,
                precio_total=carro.precio_total
            )
            
            # Limpiar el carro después del pago exitoso
            carro.limpiar_carro()
            
            messages.success(request, "Pago realizado con éxito. ¡Reserva confirmada!")
            return redirect('Home')
        else:
            messages.error(request, f"Error al procesar el pago: {result.message}")
            return redirect('carro:detalle')

    client_token = generar_client_token()
    return render(request, 'pago/confirmar_reserva.html', {'client_token': client_token})

