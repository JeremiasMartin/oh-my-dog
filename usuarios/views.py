from django.shortcuts import render
from usuarios.models import Cliente, Usuario
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from .forms import ClienteRegistroForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponseRedirect

# Create your views here.

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'admin/listar_clientes.html', {"clientes":clientes})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'cliente/login.html', {'form': form})


def user_logout(request):
    
    django_logout(request)
    return redirect('/')



def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            # Crear un usuario a partir del email y la contraseña proporcionados por el cliente
            usuario = Usuario.objects.create_user(
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password1')
            )
            # Crear un cliente asociado al usuario
            cliente = Cliente.objects.create(
                user=usuario,
                dni=form.cleaned_data.get('dni'),
                nombre=form.cleaned_data.get('nombre'),
                apellido=form.cleaned_data.get('apellido'),
                telefono=form.cleaned_data.get('telefono')
            )
            # Redirigir a la lista de clientes
            return redirect('/admin/listar_clientes')
    else:
        form = ClienteRegistroForm()

    context = {'form': form}
    return render(request, 'admin/registrar_cliente.html', context)



@login_required
def ver_perfil(request):
    usuario = request.user
    perfil = Cliente.objects.get(user=usuario)
    return render(request, 'ver_perfil_cliente.html', {"perfil":perfil})


# @login_required
# def editar_perfil(request):
#     # dictionary for initial data with
#     # field names as keys
#     context ={}
 
#     usuario = request.user

#     perfil = Cliente.objects.get(user=usuario) 

 
#     # pass the object as instance in form
#     form = EditarPerfilForm(request.POST or None , request.FILES , instance = perfil)


#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():

#         perfil.nombre = form.cleaned_data.get('nombre')
#         perfil.apellido = form.cleaned_data.get('apellido')
#         perfil.telefono = form.cleaned_data.get('telefono')
#         perfil.save()
#         return HttpResponseRedirect("/cliente/ver_perfil_cliente/")
 
#     # add form dictionary to context
#     context["form"] = form
 
#     return render(request,'ver_perfil_cliente.html', context) 