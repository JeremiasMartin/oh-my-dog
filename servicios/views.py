from django.shortcuts import render
from .models import Personal

def mapa(request):
    personal = Personal.objects.all()  # Obtener todos los objetos Personal

    context = {
        'personal': personal,
    }

    return render(request, 'mapa.html', context)
