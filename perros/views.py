from django.shortcuts import render, get_object_or_404, redirect
from .models import Perro 
from usuarios.models import Cliente
from .forms import registrar_perro
from django.contrib import messages
from django.core.paginator import Paginator

def listar_mascotas(request):
    mascotas = Perro.objects.all()
    paginator = Paginator(mascotas,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_mascotas.html', {"mascotas":page_obj})

#def registrar_atencion(request):

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