from django.urls import path
from . import views


urlpatterns = [
    path('', views.catalogo_viviendas, name='catalogo_viviendas'),
    path('detalle/<int:id>/', views.detalle_vivienda, name='detalle_vivienda'),
    path('propietario/', views.catalogo_viviendas_propietario, name='catalogo_viviendas_propietario'),
    path('propietario/detalle/<int:id>/', views.detalle_vivienda_propietario, name='detalle_vivienda_propietario'),
    path('propietario/create/', views.crear_vivienda, name='crear_vivienda'),
    path('historial_reservas/', views.historial_reservas, name='historial_reservas'),
    #path('hacer_reserva/', views.hacer_reserva, name='hacer_reserva'),
]
