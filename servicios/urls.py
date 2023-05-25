from django.urls import path
from usuarios.views import *
from . import views

urlpatterns = [
    path('mapa/', views.mapa, name='Mapa'),
]