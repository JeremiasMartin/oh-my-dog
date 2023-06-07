from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('publicar_adopcion/', views.publicar_adopcion, name='publicar_adopcion'),
    path('listar_mis_publicaciones_adopcion/',views.listar_mis_publicaciones_adopcion, name= 'listar_mis_publicaciones_adopcion'),
    path('listar_adopciones/', views.listar_adopciones, name='listar_adopciones'),
    path('postularse/<int:adopcion_id>/', views.postularse, name='postularse'),
    path('listar_postulantes_adopcion/<int:adopcion_id>/', views.listar_postulantes_adopcion, name='listar_postulantes_adopcion'),
    path('seleccionar_postulante_adopcion/<int:postulante_id>/', views.seleccionar_postulante_adopcion, name='seleccionar_postulante_adopcion'),
    path('editar_adopcion/<int:adopcion_id>/', views.editar_adopcion, name='editar_adopcion')
]