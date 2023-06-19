from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registrar_mascota_cruza/', views.registrar_mascota_cruza, name='Registrar_mascota_cruza'),
]