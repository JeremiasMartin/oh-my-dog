from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from turnos.views import paginar
from .models import Cruza
from .forms import CruzaForm
from publicaciones.models import Perro_publicacion, Publicacion


def listar_mis_mascotas_cruza(request):
    mascotas = Cruza.objects.filter(publicacion__id_usuario=request.user.id)
    contexto = {
        "cruzas":paginar(request, mascotas, 3),
    }
    return render(request, 'mis_mascotas_cruza.html', contexto)

def registrar_mascota_cruza(request):
    if request.method == 'POST':
        form = CruzaForm(request.POST, request.FILES)
        if form.is_valid():
            perro_publicacion = Perro_publicacion(
                nombre=form.cleaned_data.get('nombre'),
                tamanio=form.cleaned_data.get('tamanio'),
                sexo=form.cleaned_data.get('sexo'),
                color=form.cleaned_data.get('color'),
                edad=form.cleaned_data.get('edad'),
                raza=form.cleaned_data.get('raza'),
                foto=request.FILES.get('foto')
            )
            perro_publicacion.save()

            if (perro_publicacion.sexo == 'H'):
                periodo_celo=form.cleaned_data.get('periodo_celo')
            else:
                periodo_celo=None

            publicacion = Publicacion(
                descripcion=periodo_celo,
                id_usuario=request.user,
                id_perro_publicacion=perro_publicacion,
                activo=True,
            )
            publicacion.save()

            cruza = Cruza(
                publicacion=publicacion,
            )
            cruza.save()

            messages.success(request, 'Registro exitoso')
            return redirect('Mis_mascotas_cruza')
        else:
            messages.error(request, 'Debe completar todos los campos')
    else:
        form = CruzaForm()
        
    return render(request, 'registrar_mascota_cruza.html', {'form': form})

