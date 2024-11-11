from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vivienda
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vivienda
from django.contrib.auth.decorators import login_required
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


@login_required
def catalogo_viviendas_propietario(request):
    es_propietario = request.user.groups.filter(name='Propietario').exists()
    if not es_propietario:
        return redirect('Home')
    viviendas = Vivienda.objects.filter(propietario=request.user)
    return render(request, "catalogoViviendas/catalogo_viviendas_propietario.html", {'viviendas': viviendas,'es_propietario': es_propietario})


@login_required
def detalle_vivienda_propietario(request, id):
    vivienda = get_object_or_404(Vivienda, id=id)

    es_propietario_de_la_vivienda = request.user == vivienda.propietario
    
    if not es_propietario_de_la_vivienda:
        return redirect('Home')
    
    return render(request, "catalogoViviendas/detalle_vivienda_propietario.html", {
        'vivienda': vivienda
    })