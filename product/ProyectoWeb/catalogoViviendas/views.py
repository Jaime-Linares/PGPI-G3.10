from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Vivienda, Reserva
from .forms import ViviendaForm, ReservaForm
from django.utils import timezone
from carro.carro import Carro
from django.core.mail import EmailMessage


# --- CLIENTE ---------------------------------------------------------------------------------------------------------------------
@login_required
def catalogo_viviendas(request):
    # comprobamos si es cliente
    es_cliente = request.user.groups.filter(name='Cliente').exists()
    if not es_cliente:
        return redirect('Home')
    # miramos si estamos filtrando
    query = request.GET.get('q')
    ubicacion = request.GET.get('ubicacion')
    # filtros por nombre y ubicación
    viviendas = Vivienda.objects.all()
    if query:
        viviendas = viviendas.filter(nombre__icontains=query)
    if ubicacion:
        viviendas = viviendas.filter(ubicacion__icontains=ubicacion)
    # renderizamos
    return render(request, "catalogoViviendas/cliente/catalogo_viviendas_cliente.html", {'viviendas': viviendas,'es_cliente': es_cliente})


@login_required
def detalle_vivienda(request, id):
    es_cliente = request.user.groups.filter(name='Cliente').exists()
    if not es_cliente:
        return redirect('Home')
    
    carro = Carro(request)
    vivienda = get_object_or_404(Vivienda, id=id)
    reservas = Reserva.objects.filter(vivienda=vivienda)
    fechas_reservadas = [(reserva.fecha_inicio.strftime('%d-%m-%Y'), reserva.fecha_fin.strftime('%d-%m-%Y')) for reserva in reservas]

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            # validaciones
            error = validar_reserva(vivienda, fecha_inicio, fecha_fin)
            if error:
                form.add_error(None, error)
            else:
                if carro.reserva_existente():
                    messages.error(request, "Ya tienes una reserva en tu carrito.")
                    return render(request, "catalogoViviendas/cliente/detalle_vivienda_cliente.html", {
                        'vivienda': vivienda,
                        'form': form,
                        'fechas_reservadas': fechas_reservadas
                    })
                else:
                    dias_reserva = (fecha_fin - fecha_inicio).days + 1
                    precio_total = dias_reserva * vivienda.precio_por_dia
                    carro.agregar_reserva(vivienda, fecha_inicio, fecha_fin, precio_total)
                    messages.success(request, "Reserva añadida al carrito.")
                    return redirect('carro:detalle')
    else:
        form = ReservaForm()

    return render(request, "catalogoViviendas/cliente/detalle_vivienda_cliente.html", {
        'vivienda': vivienda,
        'form': form,
        'fechas_reservadas': fechas_reservadas
    })


def validar_reserva(vivienda, fecha_inicio, fecha_fin):
    # la fecha de fin no puede ser anterior o igual a la fecha de inicio
    if fecha_fin <= fecha_inicio:
        return "La fecha de fin debe ser posterior a la fecha de inicio."
    # no se puede reservar fechas en el pasado
    if fecha_inicio < timezone.now().date() or fecha_fin < timezone.now().date():
        return "No se puede realizar una reserva en fechas pasadas."
    # no reservar si el rango de fechas se superpone con otras reservas de la misma vivienda
    reservas_existentes = Reserva.objects.filter(
        vivienda=vivienda,
        fecha_inicio__lte=fecha_fin,
        fecha_fin__gte=fecha_inicio
    )
    if reservas_existentes.exists():
        return "Algunas fechas seleccionadas ya están reservadas para esta vivienda."
    # si todas las validaciones pasan, retornar None
    return None


@login_required
def historial_reservas(request):
    es_cliente = request.user.groups.filter(name='Cliente').exists()
    if not es_cliente:
        return redirect('Home')
    
    reservas = Reserva.objects.filter(usuario=request.user).order_by('fecha_inicio')
    today = timezone.now().date()
    for reserva in reservas:
        reserva.puede_eliminarse = reserva.fecha_inicio > today and (reserva.fecha_inicio - today).days > 7
    return render(request, "catalogoViviendas/cliente/historial_reservas.html", {'reservas': reservas, 'today': today})


@login_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    
    if reserva.fecha_inicio > timezone.now().date() and (reserva.fecha_inicio - timezone.now().date()).days > 7:
        reserva.delete()
        messages.success(request, "Reserva cancelada con éxito.")

        email = EmailMessage(
            "Cancelación de reserva en CityScape Rentals",
            f"""
            Estimado/a {request.user.username},

            Lamentamos informarte que tu reserva ha sido cancelada. A continuación, te proporcionamos los detalles de la reserva cancelada:

            - Vivienda: {reserva.vivienda.nombre}
            - Fecha de inicio: {reserva.fecha_inicio}
            - Fecha de fin: {reserva.fecha_fin}
            - Precio Total: {reserva.precio_total} €

            Si esta cancelación fue un error o necesitas realizar una nueva reserva, no dudes en contactarnos. Estamos aquí para ayudarte.

            Saludos cordiales,  
            El equipo de CityScape Rentals
            """,
            "noreply@cityscaperentals.com",
            [request.user.email],
            reply_to=["cityscapeg3@gmail.com"]
        )
    
        try:
            email.send()
            messages.success(request, "Se ha enviado la confirmación de cancelación correctamente.")
            return redirect('Home')
        except:
            messages.error(request, "Hubo un error al enviar el correo de cancelación.")
            return redirect('catalogoViviendas:historial_reservas')

    else:
        messages.error(request, "No puedes cancelar esta reserva.")
    
    return redirect('catalogoViviendas:historial_reservas')


# --- PROPIETARIO -----------------------------------------------------------------------------------------------------------------
@login_required
def catalogo_viviendas_propietario(request):
    es_propietario = request.user.groups.filter(name='Propietario').exists()
    if not es_propietario:
        return redirect('Home')
    # miramos si estamos filtrando
    query = request.GET.get('q')
    ubicacion = request.GET.get('ubicacion')
    # filtros por nombre y ubicación
    viviendas = Vivienda.objects.filter(propietario=request.user)
    if query:
        viviendas = viviendas.filter(nombre__icontains=query)
    if ubicacion:
        viviendas = viviendas.filter(ubicacion__icontains=ubicacion)
    # renderizamos
    return render(request, "catalogoViviendas/propietario/catalogo_viviendas_propietario.html", {'viviendas': viviendas,'es_propietario': es_propietario})


@login_required
def detalle_vivienda_propietario(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)
    reservas = Reserva.objects.filter(vivienda=vivienda)
    fechas_reservadas = [(reserva.fecha_inicio.strftime('%d-%m-%Y'), reserva.fecha_fin.strftime('%d-%m-%Y'), reserva.usuario.username) for reserva in reservas]

    if request.user != vivienda.propietario:
        return redirect('Home')

    if request.method == 'POST':
        form = ViviendaForm(request.POST, request.FILES, instance=vivienda)
        if form.is_valid():
            form.save()
            return redirect('catalogoViviendas:catalogo_viviendas_propietario')
    else:
        form = ViviendaForm(instance=vivienda)

    return render(request, "catalogoViviendas/propietario/detalle_vivienda_propietario.html", {
        'form': form,
        'vivienda': vivienda,
        'fechas_reservadas': fechas_reservadas
    })


@login_required
def crear_vivienda(request):
    es_propietario = request.user.groups.filter(name='Propietario').exists()
    if not es_propietario:
        return redirect('Home')

    if request.method == 'POST':
        form = ViviendaForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_vivienda = form.save(commit=False)
            nueva_vivienda.propietario = request.user
            nueva_vivienda.save()
            return redirect('catalogoViviendas:catalogo_viviendas_propietario')
    else:
        form = ViviendaForm()

    return render(request, "catalogoViviendas/propietario/crear_vivienda.html", {
        'form': form
    })


@login_required
def eliminar_vivienda(request, id):
    vivienda = get_object_or_404(Vivienda, id=id, propietario=request.user)
    if request.user != vivienda.propietario:
        return redirect('Home')
    
    if request.method == 'POST':
        vivienda.delete()
        messages.success(request, "Vivienda eliminada con éxito.")
        return redirect('catalogoViviendas:catalogo_viviendas_propietario')
    else:
        return redirect('catalogoViviendas:detalle_vivienda_propietario', id=id)

