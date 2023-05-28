from django.urls import path
from . import views

urlpatterns = [
    
    path('adoptar_perro/', views.adoptar_perro, name='adoptar_perro'),
]