from django.shortcuts import render
from usuarios.models import Cliente, Usuario
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from .forms import ClienteRegistroForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from email.mime.image import MIMEImage
from django.template.loader import get_template
from OhMyDog import settings
from django.core.mail import EmailMultiAlternatives
import os
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy

# Create your views here.

def listar_clientes(request):
    clientes = Cliente.objects.all()
    paginator = Paginator(clientes,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/listar_clientes.html', {"clientes":page_obj})



def user_login(request):   
    if request.method == "POST":
        form = UserSign(data=request.POST)
        if form.is_valid(): 
            mail = form.cleaned_data.get("email")
            contraseña = form.cleaned_data.get("password")
            user = authenticate(request, email=mail, password=contraseña)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Alguna/s de las credenciales ingresadas son incorrectas.")  
        else: 
            messages.error(request, "informacion")
    form = UserSign()     
    context = {'form' : form}
    return render(request, 'cliente/login.html', context)


def user_logout(request):
    
    django_logout(request)
    return redirect('/')



def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            # Crear un usuario a partir del email y la contraseña proporcionados por el cliente
            passwd = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
            usuario = Usuario.objects.create_user(
                email=form.cleaned_data.get('email'),
                password = passwd
            )
            cliente = Cliente.objects.create(
                user=usuario,
                dni=form.cleaned_data.get('dni'),
                nombre=form.cleaned_data.get('nombre'),
                apellido=form.cleaned_data.get('apellido'),
                telefono=form.cleaned_data.get('telefono')
            )
            subject = 'Registro de Usuario Exitoso'
            from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
            to_email = '%s' % (form.cleaned_data.get('email'))
            reply_to_email = 'noreply@ejtechsoft.com'

            image_dir = os.path.join(settings.BASE_DIR, 'OhMyDogApp', 'static', 'OhMyDogApp', 'img')
            image_name = 'logo.png'

            context = {
                    'nombre' : form.cleaned_data.get('nombre'),
                    'password'  : passwd
                    }
            text_content = get_template('cliente/mail_bienvenida.txt')
            html_content = get_template('cliente/mail_bienvenida.html')
            text_content = text_content.render(context)
            html_content = html_content.render(context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
            email.mixed_subtype = 'related'
            email.content_subtype = 'html'
            email.attach_alternative(html_content, 'text/html')

            file_path = os.path.join(image_dir, image_name)
            with open(file_path, 'rb') as f:
                image = MIMEImage(f.read())
                image.add_header('Content-ID', '<%s>' % (image_name))
                image.add_header('Content-Disposition', 'inline', filename=image_name)
                email.attach(image)

            email.send(fail_silently=False)
            messages.success(request, 'Registro exitoso')
            return redirect("/usuarios/clientes")
    else:
        form = ClienteRegistroForm()
    context = {'form': form}
    return render(request, 'admin/registrar_cliente.html',context)



@login_required
def ver_perfil(request):
    usuario = request.user
    perfil = Usuario.objects.get(id=usuario.id)
    return render(request, 'ver_perfil.html', {"usuario":perfil})


@login_required
def editar_perfil(request):
    perfil = request.user.cliente
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.save()
            messages.success(request,"¡Información actualizada correctamente!")
            return redirect('Ver_perfil')
    else:
        form = EditarPerfilForm(instance=perfil)
    return render(request, 'cliente/editar_perfil.html', {'form': form})




class cambiar_contrasenia(PasswordChangeView):
      form_class = PasswordChangeForm
      success_url ="/usuarios/ver_perfil/"

class LoginAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('/usuarios/login/')

login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())



def restablecer_contraseña(request):   
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)
        if form.is_valid(): 
            mail = form.cleaned_data.get("email")
            if Usuario.objects.filter(email=mail).exists():
                form.save(from_email='blabla@blabla.com', email_template_name='registration/password_reset_email.html', request=request)
                return redirect('/usuarios/restablecer_contrasenia_enviado')          
            else:
                messages.error(request, " El mail ingresado no se encuentra registrado en el sistema ")  
        else: 
              messages.error(request, " No existe ese mail") 
    form =  PasswordResetForm()     
    context = {'form' : form}
    return render(request, 'cliente/restablecer_contrasenia.html', context)     
     
      
class restPasswordConfirm(PasswordResetConfirmView):
      form_class = SetPasswordForm
     

def restDone(request):
    
    return render(request, 'cliente/restablecer_contrasenia_enviado.html') 

