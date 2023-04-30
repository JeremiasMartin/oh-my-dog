from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, 'OhMyDogApp/home.html')

def servicios(request):
    return render(request, 'OhMyDogApp/servicios.html')

def contacto(request):
    return render(request, 'OhMyDogApp/contacto.html')