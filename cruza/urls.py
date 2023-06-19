from django.urls import path
from . import views

urlpatterns = [
    path('registrar_mascota_cruza/', views.registrar_mascota_cruza, name='Registrar_mascota_cruza'),
    path('listar_mis_mascotas_cruza/', views.listar_mis_mascotas_cruza, name='Mis_mascotas_cruza'),
]