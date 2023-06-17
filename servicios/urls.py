from django.urls import path
from usuarios.views import *
from . import views

urlpatterns = [
    path('listar_personal/', views.listar_personal, name='Listar_personal'),
    path('editar_personal/<int:personal_id>/', views.editar_personal, name='Editar_personal'),
    path('cambiar_estado/<int:personal_id>/', views.cambiar_estado, name='Cambiar_estado'),
    path('contacto/<int:personal_id>/', views.enviar_consulta, name='Contacto'),
    path('mapa/', views.mapa, name='Mapa'),
]