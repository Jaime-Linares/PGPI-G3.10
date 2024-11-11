from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Vivienda
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Vivienda, Reserva
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.dateparse import parse_date

@login_required
def catalogo_viviendas(request):
    es_cliente = request.user.groups.filter(name='Cliente').exists()
    if not es_cliente:
        return redirect('Home')
    viviendas = Vivienda.objects.all()
    return render(request, "catalogoViviendas/catalogo_viviendas.html", {'viviendas': viviendas,'es_cliente': es_cliente})

@login_required
def detalle_vivienda(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)

    es_cliente = request.user.groups.filter(name='Cliente').exists()
    
    if not es_cliente:
        return redirect('Home')
    
    return render(request, "catalogoViviendas/detalle_vivienda.html", {
        'vivienda': vivienda,
        'es_cliente': es_cliente
    })
