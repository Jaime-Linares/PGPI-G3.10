from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Vivienda

@login_required
def catalogo_viviendas(request):
    
    es_cliente = request.user.groups.filter(name='Cliente').exists()
    # Redirigir si el usuario no es un cliente
    if not es_cliente:
       return redirect('Home')
    
    viviendas = Vivienda.objects.all()
   
    return render(request, "catalogoViviendas/catalogoViviendas.html", {'viviendas': viviendas, 'es_cliente': es_cliente})
    
