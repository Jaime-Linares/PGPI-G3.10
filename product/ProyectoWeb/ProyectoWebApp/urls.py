from django.urls import path
from ProyectoWebApp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="Home"),
    path('politica-privacidad/', views.politica_privacidad, name="PoliticaPrivacidad"),
    path('aviso-legal/', views.aviso_legal, name="AvisoLegal"),
    path('cookies/', views.cookies, name="Cookies"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Para que Django pueda encontrar las imágenes en la carpeta media