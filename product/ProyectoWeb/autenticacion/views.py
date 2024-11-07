from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User


# Create your views here.


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class VRegistro(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request,"registro/registro.html",{"form":form})
    

    def post(self, request):
        form = CustomUserCreationForm(request.POST) # En el request.POST se envian los datos del formulario (usuario y contraseña y email)
        if form.is_valid():
            usuario = form.save()
            login(request,usuario)
            return redirect("Home") 
        else:
            for msg in form.error_messages: #Para mostrar los errores en las validaciones del formulario
                messages.error(request,form.error_messages[msg])
                
            return render(request,"registro/registro.html",{"form":form})

def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect("Home")

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contraseña = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                return redirect("Home")
            # No mostramos mensajes de error
        return redirect("iniciar_sesion")  # Redirigimos a la misma página sin mostrar mensajes de error

    form = AuthenticationForm()
    return render(request, "login/login.html", {"form": form})

