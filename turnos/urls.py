from django.urls import path
from usuarios.views import *
from . import views

urlpatterns = [
    path('solicitar_turno/', views.solicitar_turno, name='solicitar_turno'),
    path('listar_turnos_pendientes/', views.listar_turnos_pendientes, name='listar_turnos_pendientes'),
    path('listar_turnos_confirmados/', views.listar_turnos_confirmados, name='listar_turnos_confirmados'),
    path('aceptar_turno/<int:id_turno>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar_turno/<int:id_turno>/', views.rechazar_solicitud, name='rechazar_solicitud'),

]