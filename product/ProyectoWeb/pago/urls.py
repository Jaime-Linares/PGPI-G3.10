from django.urls import path
from . import views

app_name = 'pago'

urlpatterns = [
    path('confirmar_reserva/', views.confirmar_reserva, name='confirmar_reserva'),
]
