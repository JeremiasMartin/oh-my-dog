from django.urls import path
from usuarios.views import *
from .views import solicitar_turno

urlpatterns = [
    path('solicitar_turno/', solicitar_turno, name='solicitar_turno'),

]