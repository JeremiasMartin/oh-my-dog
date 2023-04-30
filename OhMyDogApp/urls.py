from django.urls import path
from OhMyDogApp.views import *

urlpatterns = [
    path('', home, name="Home"),
    path('servicios', servicios, name="Servicios"),
    path('contacto', contacto, name="Contacto"),
]