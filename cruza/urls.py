from django.urls import path
from . import views

urlpatterns = [
    path('registrar_mascota_cruza/', views.registrar_mascota_cruza, name='Registrar_mascota_cruza'),
    path('listar_mis_mascotas_cruza/', views.listar_mis_mascotas_cruza, name='Mis_mascotas_cruza'),
    path('editar_mascota_cruza/<int:id_publicacion>/', views.editar_perfil_mascota_cruza, name='Editar_mascota_cruza'),
    path('listar_recomendados/<int:id_publicacion>/', views.listar_recomendados, name='Recomendados'),
    path('postularse_mascota_cruza/<int:publicacion_a_postular>/<int:postulante>', views.postularse_mascota_cruza, name='Postularse_cruza'),
    path('cambiar_estado_publicacion/<int:id_publicacion>/', views.cambiar_estado_publicacion, name='Cambiar_estado_publicacion'),
]