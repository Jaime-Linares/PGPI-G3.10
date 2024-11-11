from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vivienda
from .forms import ViviendaForm



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
