
# Create your views here.
import braintree
from django.shortcuts import render, redirect
from django.contrib import messages
from carro.carro import Carro

def generar_client_token():
    return braintree.ClientToken.generate()

def confirmar_reserva(request):
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce')
        carro = Carro(request)
        total = float(request.session.get('importe_total_carro', 0))

        # Procesar el pago con Braintree
        result = braintree.Transaction.sale({
            "amount": f"{total:.2f}",
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            carro.limpiar()  # Limpiar el carrito después del pago
            messages.success(request, "Pago realizado con éxito. ¡Reserva confirmada!")
            return redirect('Home')
        else:
            messages.error(request, "Error al procesar el pago. Inténtalo de nuevo.")

    client_token = generar_client_token()
    return render(request, 'pago/confirmar_reserva.html', {'client_token': client_token})
