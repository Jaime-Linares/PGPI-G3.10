from django.shortcuts import render
from .forms import FormularioContacto
from django.shortcuts import redirect
from django.core.mail import EmailMessage

# Create your views here.

def contacto(request):
    formularioContacto = FormularioContacto()

    if request.method == "POST":
        formularioContacto = FormularioContacto(data=request.POST)
        if formularioContacto.is_valid():
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')   
            contenido = request.POST.get('contenido')

            email = EmailMessage("Contacto CityScape Rentals", 
                                 "El usuario con nombre {} con la dirección de correo {} escribe lo siguiente:\n\n{}".format(nombre, email, contenido),
                                 "", # Aquí se puede poner el correo de quien viene el mensaje, pero en este caso se deja vacío ya que lo tenemos en settings.py
                                 ["cityscapeg3@gmail.com"],reply_to=[email]) 
            # Si nos llega bien el email entra por el try
            try:
                email.send()
                return redirect("/contacto/?valido") # Esta línea es para redirigir a la misma página con un mensaje de éxito una vez que se haya enviado el formulario
            except:
                return redirect("/contacto/?novalido")



    return render(request, "contacto/contacto.html", {"miFormulario": formularioContacto})

