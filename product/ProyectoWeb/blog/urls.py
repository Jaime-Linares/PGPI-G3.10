   

from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog, name="Blog"),
    path('categoria/<int:categoria_id>/', views.categoria, name="categoria"), # el int creo que no hace falta 

]


