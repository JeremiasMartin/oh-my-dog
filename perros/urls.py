from django.urls import path
from . import views

urlpatterns = [
    path('registrar-mascota/<int:cliente_id>/', views.registrar_mascota, name="Registro_mascota"),
    path('listar-mascotas/', views.listar_mascotas, name='Mascotas'),
    path('listar-mascotas-cliente/<int:cliente_id>/', views.listar_mascotas_cliente, name='Listar_mascotas_cliente'),
    path('editar-perfil-mascota/<int:id>/', views.editar_perfil_mascota, name="Editar_perfil_mascota"),
    path('registrar-atencion/<int:id_mascota>/', views.registrar_atencion, name="Registro_atencion"),
]