from django.urls import path
from OhMyDogApp.views import *

urlpatterns = [
    path('', home, name="Home"),
]