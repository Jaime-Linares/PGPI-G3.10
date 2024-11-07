from django.shortcuts import render,HttpResponse
from carro.carro import Carro

# Create your views here.

def home(request):
    carro = Carro(request) # Para que no salga un error del carro en las sesiones, mejor es crear un carro vacío al arrancar la aplicación para que no salga error
    return render(request, "ProyectoWebApp/home.html")



