from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from pedidos.models import LineaPedido, Pedido
from carro.carro import Carro
# Create your views here.

@login_required(login_url='autenticacion/iniciar_sesion')
def procesar_pedido(request):
    pedido = Pedido.objects.create(user=request.user)
    carro=Carro(request)
    lineas_pedido = list()
    for key, value in carro.carro.items():
        lineas_pedido.append(LineaPedido(
            user=request.user,
            producto_id=key,
            pedido=pedido,
            cantidad=value['cantidad']
        ))
    
    LineaPedido.objects.bulk_create(lineas_pedido) # Este método es como hacer muchos inserts en una sola consulta
    enviar_mail(
                pedido=pedido,
                lineas_pedido=lineas_pedido,
                nombreusuario=request.user.username,
                emailusuario=request.user.email)
    messages.success(request, 'Pedido procesado correctamente')
    
    return redirect('../tienda')


def enviar_mail(**kwargs):
    asunto = "Gracias por el pedido"
    mensaje = render_to_string("emails/pedido.html", {
        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "nombreusuario": kwargs.get("nombreusuario"),
        "emailusuario": kwargs.get("emailusuario"),
    })
    mensaje_texto = strip_tags(mensaje)
    from_email = "toxicodivi@gmail.com"
    to = kwargs.get("emailusuario")
    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)
