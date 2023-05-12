from django.urls import path
from usuarios.views import *
from . import views

urlpatterns = [
    path('solicitar_turno/', views.solicitar_turno, name='solicitar_turno'),
     

]