from django.urls import path
from . import views

urlpatterns = [
    path('', views.detalle_profile, name='detalle_profile')
]