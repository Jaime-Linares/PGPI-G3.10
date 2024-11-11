from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Vivienda
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Vivienda, Reserva
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
import json
from datetime import datetime, timedelta

@login_required
def catalogo_viviendas(request):
    es_cliente = request.user.groups.filter(name='Cliente').exists()
    if not es_cliente:
        return redirect('Home')
    viviendas = Vivienda.objects.all()
    return render(request, "catalogoViviendas/catalogo_viviendas.html", {'viviendas': viviendas,'es_cliente': es_cliente})




def detalle_vivienda(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)
    reservas = Reserva.objects.filter(vivienda=vivienda)

    fechas_reservadas = [reserva.fecha_inicio.strftime('%Y-%m-%d') for reserva in reservas]

    return render(request, "catalogoViviendas/detalle_vivienda.html", {
        'vivienda': vivienda,
        'fechas_reservadas': json.dumps(fechas_reservadas),
    })


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
