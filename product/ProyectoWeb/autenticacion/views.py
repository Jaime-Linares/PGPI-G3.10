from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[('Propietario', 'Propietario'), ('Cliente', 'Cliente')],
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            role = self.cleaned_data["role"]
            group = Group.objects.get(name=role)
            user.groups.add(group)
        return user


class VRegistro(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registro/registro.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("Home") 
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
                
            return render(request, "registro/registro.html", {"form": form})


def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect("Home")


def iniciar_sesion(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")

        usuario = authenticate(username=username_or_email, password=password)
        
        # Si no encuentra por nombre de usuario, intenta buscar por email
        if usuario is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                usuario = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                usuario = None

        if usuario is not None:
            login(request, usuario)
            return redirect("Home")
        return redirect("iniciar_sesion")

    form = AuthenticationForm()
    return render(request, "login/login.html", {"form": form})

