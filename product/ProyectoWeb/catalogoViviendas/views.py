from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Vivienda, Reserva
from django.utils.dateparse import parse_date
from .forms import ViviendaForm, ReservaForm


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
    return render(request, "catalogoViviendas/catalogo_viviendas_cliente.html", {'viviendas': viviendas,'es_cliente': es_cliente})


@login_required
def detalle_vivienda(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)
    reservas = Reserva.objects.filter(vivienda=vivienda)
    fechas_reservadas = [reserva.fecha_inicio.strftime('%Y-%m-%d') for reserva in reservas]

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            # Validar que las fechas no estén ya reservadas
            reservas_existentes = Reserva.objects.filter(
                vivienda=vivienda,
                fecha_inicio__lte=fecha_fin,
                fecha_fin__gte=fecha_inicio
            )

            if reservas_existentes.exists():
                form.add_error(None, 'Algunas fechas seleccionadas ya están reservadas')
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

                return render(request, "catalogoViviendas/reserva_exitosa.html", {
                    'vivienda': vivienda,
                    'precio_total': precio_total
                })
    else:
        form = ReservaForm()

    return render(request, "catalogoViviendas/detalle_vivienda_cliente.html", {
        'vivienda': vivienda,
        'form': form,
        'fechas_reservadas': fechas_reservadas
    })


@login_required
def hacer_reserva(request):
    if request.method == 'POST':
        vivienda_id = request.POST.get('vivienda_id')
        fecha_inicio = parse_date(request.POST.get('fecha_inicio'))
        fecha_fin = parse_date(request.POST.get('fecha_fin'))
        vivienda = Vivienda.objects.get(id=vivienda_id)

        dias_reserva = (fecha_fin - fecha_inicio).days + 1
        precio_total = dias_reserva * vivienda.precio_por_dia

        Reserva.objects.create(
            vivienda=vivienda,
            usuario=request.user,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            precio_total=precio_total
        )

        return JsonResponse({'success': True, 'precio_total': precio_total})
    return JsonResponse({'success': False})


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
    return render(request, "catalogoViviendas/catalogo_viviendas_propietario.html", {'viviendas': viviendas,'es_propietario': es_propietario})


@login_required
def detalle_vivienda_propietario(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)

    if request.user != vivienda.propietario:
        return redirect('Home')

    if request.method == 'POST':
        form = ViviendaForm(request.POST, request.FILES, instance=vivienda)
        if form.is_valid():
            form.save()
            return redirect('catalogo_viviendas_propietario')
    else:
        form = ViviendaForm(instance=vivienda)

    return render(request, "catalogoViviendas/detalle_vivienda_propietario.html", {
        'form': form,
        'vivienda': vivienda
    })
