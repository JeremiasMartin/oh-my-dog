from django.shortcuts import render
from .models import Personal
from django.core.paginator import Paginator
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from turnos.views import paginar

def listar_personal(request):
    personal = Personal.objects.all()
    return render(request, 'listar_personal.html', {"personal":paginar(request,personal,6)})

def cambiar_estado(request, personal_id):
    personal = Personal.objects.get(id=personal_id)
    if(personal.activo):
        personal.activo = False
    else:
        personal.activo = True
    personal.save()
    return redirect('/servicios/listar_personal')


def editar_personal(request, personal_id):
    personal = get_object_or_404(Personal, id=personal_id)
    if request.method == 'POST':
        form = PersonalEditForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            messages.success(request,"¡Información actualizada correctamente!")
            return redirect('Listar_personal')

    else:
        form = PersonalEditForm(instance=personal)
    context = {'form': form, 'errors': form.errors}

    return render(request, 'editar_personal.html', context)


def mapa(request):
    personal = Personal.objects.filter(activo=True)

    context = {
        'personal': personal,
    }

    return render(request, 'mapa.html', context)

