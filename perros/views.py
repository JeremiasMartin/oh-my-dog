from django.shortcuts import render

# Create your views here.
def registrar_mascota(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            # Crear un usuario a partir del email(que es username) y la contraseña proporcionados por el cliente
            usuario = Usuario.objects.create_user(
                username=form.cleaned_data.get('username'),
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
    return render(request, 'admin/registrar_mascota.html', context)

def registrar_atencion(request):