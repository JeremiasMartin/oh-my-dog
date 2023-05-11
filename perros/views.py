from django.shortcuts import render, get_object_or_404, redirect
from .models import Perro 
from usuarios.models import Cliente
from .forms import registrar_perro, editar_pefil_mascota, registrar_atencion_form
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime


def listar_mascotas_cliente(request, cliente_id):
    mascotas = Perro.objects.filter(cliente_id=cliente_id)
    paginator = Paginator(mascotas,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_mascotas.html', {"mascotas":page_obj})

def registrar_mascota(request, cliente_id):
    cliente = get_object_or_404(Cliente, cliente_id=cliente_id)
    if request.method == 'POST':
        # Procesar el formulario de registro de mascota
        form = registrar_perro(request.POST)
        if form.is_valid():
            # Crear la mascota y guardarla en la base de datos
            mascota = form.save(commit=False)
            mascota.cliente = cliente
            mascota.save()
            messages.success(request, 'Mascota agregada exitosamente')
            return redirect('/usuarios/clientes')
    else:
        # Mostrar el formulario de registro de mascota
        form = registrar_perro()
    
    context={
        'form': form,
        'cliente':cliente,
    }
    return render(request, 'admin/registrar_mascota.html', context)

def editar_perfil_mascota(request, id):
    perro = get_object_or_404(Perro, id=id)
    if request.method == 'POST':
        form = editar_pefil_mascota(request.POST, instance=perro)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Información actualizada correctamente!')
            return redirect(f"/perros/listar-mascotas-cliente/{perro.cliente.cliente_id}/")
    else:
        form = editar_pefil_mascota(instance=perro)
    
    context = {
        'form': form, 
        'perro': perro
    }
    
    return render(request, 'editar_perfil_mascota.html', context)

def registrar_atencion(request, id_mascota):
    perro = get_object_or_404(Perro, id=id_mascota)
    if request.method == 'POST':
        form = registrar_atencion_form(request.POST)
        if form.is_valid():
            atencion = form.save(commit=False)
            atencion.mascota = perro
            atencion.fecha = datetime.now()
            atencion.save()
            messages.success(request, 'Atención registrada exitosamente')
            return redirect(f'/perros/listar-mascotas-cliente/{perro.cliente.cliente_id}/')
    else:
        form = registrar_atencion_form()
    context={
        'form': form,
        'perro': perro,
    }
    return render(request, 'admin/registrar_atencion.html', context)