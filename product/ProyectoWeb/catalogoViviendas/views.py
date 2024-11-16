from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vivienda, Reserva
from .forms import ViviendaForm, ReservaForm
from django.utils import timezone


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
    
    vivienda = get_object_or_404(Vivienda, id=id)
    reservas = Reserva.objects.filter(vivienda=vivienda)
    fechas_reservadas = [(reserva.fecha_inicio.strftime('%d-%m-%Y'), reserva.fecha_fin.strftime('%d-%m-%Y')) for reserva in reservas]

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            usuario = request.user

            # validaciones
            error = validar_reserva(vivienda, usuario, fecha_inicio, fecha_fin)
            if error:
                form.add_error(None, error)
            else:
                dias_reserva = (fecha_fin - fecha_inicio).days + 1
                precio_total = dias_reserva * vivienda.precio_por_dia

                Reserva.objects.create(
                    vivienda=vivienda,
                    usuario=request.user,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    precio_total=precio_total
                )

                return render(request, "catalogoViviendas/cliente/reserva_exitosa.html", {
                    'vivienda': vivienda,
                    'precio_total': precio_total,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin
                })
    else:
        form = ReservaForm()

    return render(request, "catalogoViviendas/cliente/detalle_vivienda_cliente.html", {
        'vivienda': vivienda,
        'form': form,
        'fechas_reservadas': fechas_reservadas
    })


def validar_reserva(vivienda, usuario, fecha_inicio, fecha_fin):
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
            return redirect('catalogo_viviendas_propietario')
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
            return redirect('catalogo_viviendas_propietario')
    else:
        form = ViviendaForm()

    return render(request, "catalogoViviendas/propietario/crear_vivienda.html", {
        'form': form
    })

