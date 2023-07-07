from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('publicar_adopcion/', views.publicar_adopcion, name='publicar_adopcion'),
    path('listar_mis_publicaciones_adopcion/',views.listar_mis_publicaciones_adopcion, name= 'listar_mis_publicaciones_adopcion'),
    path('listar_adopciones/', views.listar_adopciones, name='listar_adopciones'),
    path('postularse/<int:adopcion_id>/', views.postularse, name='postularse'),
    path('listar_postulaciones_adopcion/', views.listar_mis_postulaciones, name='listar_postulaciones_adopcion'),
    path('listar_postulantes_adopcion/<int:adopcion_id>/', views.listar_postulantes_adopcion, name='listar_postulantes_adopcion'),
    path('seleccionar_postulante_adopcion/<int:postulante_id>/', views.seleccionar_postulante_adopcion, name='seleccionar_postulante_adopcion'),
    path('editar_adopcion/<int:adopcion_id>/', views.editar_adopcion, name='editar_adopcion'),
    path('publicar_perro_perdido/', views.publicar_perro_perdido, name='publicar_perro_perdido'),
    path('listar_perros_perdidos/', views.listar_perros_perdidos, name='listar_perros_perdidos'),
    path('cargar_perro_encontrado/', views.cargar_perro_encontrado, name='cargar_perro_encontrado'),
    path('listar_perros_encontrados/', views.listar_perros_encontrados, name='listar_perros_encontrados'),
    path('listar_mis_perros_encontrados/', views.listar_mis_perros_encontrados, name='listar_mis_perros_encontrados'),
    path('listar_mis_perros_perdidos/', views.listar_mis_perros_perdidos, name='listar_mis_perros_perdidos'),
    path('contactarse_perro/<int:id>/', views.contactarse_perro, name='contactarse_perro'),
    path('finalizar_publicacion/<int:id_publicacion>/', views.finalizar_publicacion, name="finalizar_publicacion"),
    path('editar_publicacion/<int:id_publicacion>/', views.editar_publicacion, name='editar_publicacion'),

]