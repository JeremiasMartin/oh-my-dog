from django.urls import path
from usuarios.views import *

urlpatterns = [
    path('', listar_clientes, name="Clientes"),
    path('login/', user_login, name='Login'),
    path('logout/', user_logout, name='Logout'),
    path('registrar_cliente/', registrar_cliente, name='Registro'),
    path('clientes/', listar_clientes, name='Clientes'),
    path('ver_perfil/', ver_perfil, name='Ver_perfil'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
]