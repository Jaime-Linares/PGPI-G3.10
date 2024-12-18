import braintree
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from carro.carro import Carro
from catalogoViviendas.models import Reserva
from django.core.mail import EmailMessage
from carro.models import Carro
import smtplib
from django.views.decorators.http import require_http_methods
from catalogoViviendas.views import validar_reserva



redirect_carro_detalle= 'carro:detalle'

def generar_client_token():
    return braintree.ClientToken.generate()

@login_required
@require_http_methods(["GET", "POST"])
def confirmar_reserva(request):
    try:
        carro = Carro.objects.get(usuario=request.user)
        total = float(carro.precio_total)
    except Carro.DoesNotExist:
        total = 0

    es_valida = validar_reserva(carro.vivienda, carro.fecha_inicio, carro.fecha_fin)
    if es_valida is not None:
        messages.error(request, es_valida)
        return redirect(redirect_carro_detalle)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce')

        # Verifica si el total es mayor que cero antes de intentar la transacción
        if total <= 0:
            messages.error(request, "El monto debe ser mayor que cero.")
            return redirect(redirect_carro_detalle)

        # Procesar el pago con Braintree
        result = braintree.Transaction.sale({
            "amount": f"{total:.2f}",
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            # Crear y guardar la reserva en la base de datos usando la información del carro
            Reserva.objects.create(
                vivienda=carro.vivienda,
                usuario=request.user,
                fecha_inicio=carro.fecha_inicio,
                fecha_fin=carro.fecha_fin,
                precio_total=carro.precio_total
            )
            
            vivienda = carro.vivienda
            fecha_inicio = carro.fecha_inicio
            fecha_fin = carro.fecha_fin
            precio_total = carro.precio_total

            # Limpiar el carro después del pago exitoso
            carro.limpiar_carro()

            messages.success(request, "Pago realizado con éxito. ¡Reserva confirmada!")

            email = EmailMessage(
                    "Confirmación de reserva en CityScape Rentals",
                    f"""
                    Estimado/a {request.user.username},

                    Gracias por realizar tu reserva con CityScape Rentals. A continuación, te proporcionamos los detalles de tu reserva:

                    - Vivienda: {vivienda.nombre}
                    - Fecha de inicio: {fecha_inicio}
                    - Fecha de fin: {fecha_fin}
                    - Precio Total: {precio_total} €

                    Si tienes alguna duda o necesitas realizar cambios en tu reserva, no dudes en contactarnos.

                    Saludos cordiales,  
                    El equipo de CityScape Rentals
                    """,
                    "noreply@cityscaperentals.com",
                    [request.user.email],
                    reply_to=["cityscapeg3@gmail.com"]
                )

            try:
                email.send()
                return render(request,'pago/reserva_exitosa.html',{'usuario': request.user ,'vivienda': vivienda, 'fecha_inicio': fecha_inicio, 
                                                               'fecha_fin': fecha_fin, 'precio_total': precio_total})
            except (smtplib.SMTPException, OSError):
                messages.error(request, f"Error al enviar el correo: {result.message}")
                return redirect(redirect_carro_detalle)

        else:
            messages.error(request, f"Error al procesar el pago: {result.message}")
            return redirect(redirect_carro_detalle)

    client_token = generar_client_token()
    return render(request, 'pago/confirmar_reserva.html', {'client_token': client_token})

