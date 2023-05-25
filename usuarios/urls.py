from django.urls import path
from usuarios.views import *
from django.contrib.auth import views

urlpatterns = [
    path('', listar_clientes, name="Clientes"),
    path('login/', user_login, name='Login'),
    path('logout/', user_logout, name='Logout'),
    path('registrar_cliente/', registrar_cliente, name='Registro'),
    path('clientes/', listar_clientes, name='Clientes'),
    path('ver_perfil/', ver_perfil, name='Ver_perfil'),
    path('editar_perfil/', editar_perfil, name='Editar_perfil'),
    path('restablecer_contrasenia/',restablecer_contraseña, name='Restablecer_contrasenia'),
    path('restablecer_contrasenia_enviado/',restDone, name='restablecer_contrasenia_enviado'),
    path('reset/<uidb64>/<token>', restPasswordConfirm.as_view(template_name='cliente/rest-contra-conf.html'), name='password_reset_confirm'),
    path('reset_password_complete/', views.PasswordResetCompleteView.as_view(template_name="cliente/restablecer_contrasenia_exitoso.html"), name='password_reset_complete'),
    path('cambiar_contrasenia/', cambiar_contrasenia.as_view(template_name='cliente/cambiar_contrasenia.html')),
    path('password_change/done/',views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('registrar_personal/', registrar_personal, name='Registrar_personal'),
]