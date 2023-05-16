from django.urls import path
from usuarios.views import *
from . import views
import threading


urlpatterns = [
    path('solicitar_turno/', views.solicitar_turno, name='solicitar_turno'),
    path('listar_turnos_pendientes/', views.listar_turnos_pendientes, name='listar_turnos_pendientes'),
    path('listar_turnos_confirmados/', views.listar_turnos_confirmados, name='listar_turnos_confirmados'),
    path('listar_confirmados_dia/', views.listar_confirmados_del_dia, name='listar_confirmados_dia'),
    path('aceptar_turno/<int:id_turno>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar_turno/<int:id_turno>/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('run_scheduler/', views.run_scheduler, name='run_scheduler'),
]

# Iniciar el hilo que ejecuta el planificador al iniciar la aplicación
threading.Thread(target=views.run_scheduler, daemon=True).start()