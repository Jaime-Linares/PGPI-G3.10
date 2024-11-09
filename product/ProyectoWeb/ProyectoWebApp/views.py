from django.shortcuts import render,HttpResponse
from carro.carro import Carro



def home(request):
    carro = Carro(request) # Para que no salga un error del carro en las sesiones, mejor es crear un carro vacío al arrancar la aplicación para que no salga error
    return render(request, "ProyectoWebApp/home.html")


def politica_privacidad(request):
    return render(request, "ProyectoWebApp/politica_privacidad.html")

