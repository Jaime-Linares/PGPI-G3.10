from django.shortcuts import render,HttpResponse
from carro.carro import Carro
from django.views.decorators.http import require_http_methods





@require_http_methods(["GET"])
def home(request):
    carro = Carro(request) # Para que no salga un error del carro en las sesiones, mejor es crear un carro vacío al arrancar la aplicación para que no salga error
    return render(request, "ProyectoWebApp/home.html")

@require_http_methods(["GET"])
def politica_privacidad(request):
    return render(request, "ProyectoWebApp/politica_privacidad.html")

@require_http_methods(["GET"])
def aviso_legal(request):
    return render(request, "ProyectoWebApp/aviso_legal.html")

@require_http_methods(["GET"])
def cookies(request):
    return render(request, "ProyectoWebApp/cookies.html")

