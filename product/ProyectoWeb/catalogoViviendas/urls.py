from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_viviendas, name='catalogo_viviendas'),
    path('detalle/<int:id>/', views.detalle_vivienda, name='detalle_vivienda'),
    path('hacer_reserva/', views.hacer_reserva, name='hacer_reserva'),
]
