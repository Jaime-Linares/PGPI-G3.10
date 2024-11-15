from django.urls import path
from . import views

urlpatterns = [
    path('', views.detalle_profile, name='detalle_profile'),
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
]