from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('adoptar_perro/', views.adoptar_perro, name='adoptar_perro'),
    path('listar_publicaciones/',views.listar_publicaciones, name= 'listar_publicaciones'),
    path('listar_adopciones/', views.listar_adopciones, name='listar_adopciones'),
    path('postularse/<int:adopcion_id>/', views.postularse, name='postularse'),

]
