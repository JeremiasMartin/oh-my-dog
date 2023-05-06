from django.urls import path
from . import views

urlpatterns = [
    path('registrar_mascota/<int:cliente_id>/', views.registrar_mascota, name="Registro_mascota"),
    path('listar_mascotas/', views.listar_mascotas, name='Mascotas'),
    path('editar_perfil_mascota/<int:id>/', views.editar_perfil_mascota, name="Editar_perfil_mascota"),
]