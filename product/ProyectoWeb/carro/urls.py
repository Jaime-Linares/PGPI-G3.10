from django.urls import path
from . import views

app_name = "carro"

urlpatterns = [
    path('eliminar/', views.eliminar_reserva_carro, name="eliminar"),
    path('detalle/', views.detalle_carro, name="detalle"),
]
