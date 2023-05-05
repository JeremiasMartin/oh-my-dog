from django.urls import path
from . import views

urlpatterns = [
    path('registrar_mascota/<int:cliente_id>/', views.registrar_mascota, name="Registro_mascota"),
    #path('ver_perfil/', views.servicios, name="Perfil Mascota"),
    path('listar_mascotas/', views.listar_mascotas, name='Mascotas')
]