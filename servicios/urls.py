from django.urls import path
from usuarios.views import *
from . import views

urlpatterns = [
    path('listar_personal/', views.listar_personal, name='Listar_personal'),
    path('editar_personal/<int:personal_id>/', views.editar_personal, name='Editar_personal'),
    path('cambiar_estado/<int:personal_id>/', views.cambiar_estado, name='Cambiar_estado'),
    path('contacto/<int:personal_id>/', views.enviar_consulta, name='Contacto'),
    path('cargar_guardias/', views.cargar_guardia, name='Cargar_guardias'),
    path('editar_guardias/', views.editar_guardia, name='Editar_guardias'),
    path('listar_guardias/', views.listar_guardias, name='Listar_guardias'),
    path('cargar_campaña/', views.cargar_campaña, name='Cargar_campaña'),
    path('editar_campaña/<int:campaña_id>/', views.editar_campaña, name='Editar_campaña'),
    path('listar_campañas/', views.listar_campañas, name='Listar_campañas'),
    path('donar/<int:campaña_id>/', views.donar, name='Donar'),
    path('donacion_exitosa/<int:campaña_id>/<int:monto>/', views.donacion_exitosa, name='Donacion_exitosa'),
    path('listar_donaciones/', views.listar_donaciones, name='Listar_donaciones'),
    path('descargar_comprobante/<int:donacion_id>/', views.descargar_comprobante, name='Descargar_comprobante'),
    path('mapa/', views.mapa, name='Mapa'),
]