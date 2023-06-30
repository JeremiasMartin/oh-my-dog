from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from turnos.views import paginar
from .forms import CruzaForm
from publicaciones.models import Perro_publicacion, Publicacion


def listar_mis_mascotas_cruza(request):
    mascotas = Publicacion.objects.filter(tipo_publicacion="Cruza", id_usuario=request.user.id)
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
                tipo_publicacion = "Cruza",
            )
            publicacion.save()

            messages.success(request, 'Registro exitoso')
            return redirect('Mis_mascotas_cruza')
        else:
            messages.error(request, 'Debe completar todos los campos')
    else:
        form = CruzaForm()
        
    return render(request, 'registrar_mascota_cruza.html', {'form': form})

def editar_perfil_mascota_cruza(request, id_publicacion):
    publicacion = get_object_or_404(Publicacion, id=id_publicacion)
    perro_publicacion = get_object_or_404(Perro_publicacion, id=publicacion.id_perro_publicacion_id)

    if request.method == 'POST':
        form = CruzaForm(request.POST, request.FILES)
        if form.is_valid() or 'foto' not in request.FILES:
            perro_publicacion.nombre = form.cleaned_data.get('nombre')
            perro_publicacion.tamanio = form.cleaned_data.get('tamanio')
            perro_publicacion.sexo = form.cleaned_data.get('sexo')
            perro_publicacion.color = form.cleaned_data.get('color')
            perro_publicacion.edad = form.cleaned_data.get('edad')
            perro_publicacion.raza = form.cleaned_data.get('raza')
            foto = form.cleaned_data.get('foto')
            if foto:
                perro_publicacion.foto = foto
            perro_publicacion.save()
            if (perro_publicacion.sexo == 'H'):
                periodo_celo=form.cleaned_data.get('periodo_celo')
            else:
                periodo_celo=None

            publicacion.descripcion = periodo_celo
            publicacion.save()

            messages.success(request, "¡Información actualizada correctamente!")
            return redirect('Mis_mascotas_cruza')
    else:
        form = CruzaForm(initial={
            'nombre': perro_publicacion.nombre,
            'tamanio': perro_publicacion.tamanio,
            'sexo': perro_publicacion.sexo,
            'color': perro_publicacion.color,
            'edad': perro_publicacion.edad,
            'raza': perro_publicacion.raza,
            'foto': perro_publicacion.foto,
            'periodo_celo': publicacion.descripcion,
        })
    return render(request, 'editar_mascota_cruza.html', {'form': form})