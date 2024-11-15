from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.detalle_profile, name='detalle_profile')
]