from django.urls import path
from . import views

app_name = 'catalogoViviendas' 


urlpatterns = [
    path('', views.catalogo_viviendas, name='catalogo_viviendas'),
    path('detalle/<int:id>/', views.detalle_vivienda, name='detalle_vivienda'),
    path('propietario/', views.catalogo_viviendas_propietario, name='catalogo_viviendas_propietario'),
    path('propietario/detalle/<int:id>/', views.detalle_vivienda_propietario, name='detalle_vivienda_propietario'),
    path('propietario/create/', views.crear_vivienda, name='crear_vivienda'),
    path('propietario/eliminar/<int:id>/', views.eliminar_vivienda, name='eliminar_vivienda'),
    path('historial_reservas/', views.historial_reservas, name='historial_reservas'),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
]
