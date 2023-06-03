from django.shortcuts import render, redirect
from .forms import AdopcionForm, PostulacionForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

def adoptar_perro(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST, request.FILES)
        if form.is_valid():
            perro_publicacion = Perro_publicacion(
                nombre=form.cleaned_data.get('nombre'),
                tamanio=form.cleaned_data.get('tamanio'),
                sexo=form.cleaned_data.get('sexo'),
                color=form.cleaned_data.get('color'),
                edad=form.cleaned_data.get('edad'),
                raza=form.cleaned_data.get('raza'),
                foto=form.cleaned_data.get('foto'),
            )
            perro_publicacion.save()

            publicacion = Publicacion(
                descripcion=form.cleaned_data.get('motivo_adopcion'),
                id_usuario=request.user,
                id_perro_publicacion=perro_publicacion,
                activo=True,
            )
            publicacion.save()

            adopcion = Adopcion(
                id_publicacion=request.user,
                perro_publicacion=perro_publicacion,
                motivo_adopcion=form.cleaned_data.get('motivo_adopcion'),
                origen=form.cleaned_data.get('origen'),
            )
            adopcion.save()

            messages.success(request, 'Subido exitosamente')
            return redirect('/')
        else:
            messages.error(request, 'Debe completar todos los campos')
    else:
        form = AdopcionForm()
        
    return render(request, 'adoptar_perro.html', {'form': form})




@login_required
def listar_publicaciones(request):
    adopciones =adopciones = Adopcion.objects.select_related('perro_publicacion').filter(id_publicacion_id=request.user.id)
    return render(request, 'listar_publicaciones.html', {'adopciones': adopciones})
    

@login_required
def listar_adopciones(request):
    adopciones = Adopcion.objects.filter(perro_publicacion__publicacion__activo=True)
    return render(request, 'listar_adopciones.html', {'adopciones': adopciones})

@login_required

def postularse(request, adopcion_id):
    adopcion = Adopcion.objects.get(id=adopcion_id)
    if adopcion.id_publicacion_id == request.user.id:
        messages.error(request, 'No puedes postularte a tu propia publicación.')
        return redirect('listar_adopciones')
    if request.method == 'POST':
        form = PostulacionForm(request.POST)
        if form.is_valid():
            adopcion = get_object_or_404(Adopcion, id=adopcion_id)
            postulacion = form.save(commit=False)
            postulacion.cliente = request.user
            postulacion.publicacion_adopcion = adopcion
            postulacion.save()
            return redirect('listar_adopciones')
    else:
        form = PostulacionForm()
    return render(request, 'postularse.html', {'form': form, 'adopcion_id': adopcion_id})
