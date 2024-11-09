from django.shortcuts import render,HttpResponse
from carro.carro import Carro



def home(request):
    carro = Carro(request) # Para que no salga un error del carro en las sesiones, mejor es crear un carro vacío al arrancar la aplicación para que no salga error
    return render(request, "ProyectoWebApp/home.html")


def politica_privacidad(request):
    return render(request, "ProyectoWebApp/politica_privacidad.html")


def aviso_legal(request):
    return render(request, "ProyectoWebApp/aviso_legal.html")


def cookies(request):
    return render(request, "ProyectoWebApp/cookies.html")

