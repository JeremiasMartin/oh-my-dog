from django.shortcuts import render
from .models import Personal
from django.core.paginator import Paginator
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from turnos.views import paginar
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import datetime
import mercadopago
from mercadopago.config import RequestOptions

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


def enviar_consulta(request, personal_id):
    person = get_object_or_404(Personal, id=personal_id)

    if request.method == 'POST':
        consulta = request.POST.get('consulta')
        subject = 'Consulta ¡Oh My Dog!'

        if request.user.is_authenticated:
            from_email = request.user.email
        else:
            from_email = request.POST.get('email')

        to_email = person.email
        reply_to_email = 'noreply@ejtechsoft.com'

        context = {
            'consulta': consulta,
            'mail_consulta': from_email,
        }   
        
        text_content = get_template('mail/consulta_mail.txt')
        html_content = get_template('mail/consulta_mail.html')
        text_content = text_content.render(context)
        html_content = html_content.render(context)

        email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
        email.mixed_subtype = 'related'
        email.content_subtype = 'html'
        email.attach_alternative(html_content, 'text/html')
        email.send(fail_silently=False)
        messages.success(request, "¡Consulta enviada correctamente!")
        return redirect('Contacto', personal_id=personal_id)
    else:
        return render(request, 'enviar_consulta.html', {'person': person})


def mapa(request):
    personal = Personal.objects.filter(activo=True)

    context = {
        'personal': personal,
    }

    return render(request, 'mapa.html', context)

def cargar_guardia(request):
    guardia = Guardia.objects.first()

    if request.method == 'POST':
        form = GuardiaForm(request.POST, instance=guardia)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Guardia cargada correctamente!")
            return redirect('Listar_guardias')

    else:
        form = GuardiaForm(instance=guardia)

    context = {'form': form, 'errors': form.errors}
    return render(request, 'cargar_guardia.html', context)


def listar_guardias(request):
    guardias = Guardia.objects.all()
    return render(request, 'listar_guardias.html', {"guardias":guardias, "fecha":datetime.datetime.now()})

def editar_guardia(request):
    guardia = Guardia.objects.first()

    if request.method == 'POST':
        form = GuardiaForm(request.POST, instance=guardia)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Guardia editada correctamente!")
            return redirect('Listar_guardias')
    else:
        form = GuardiaForm(instance=guardia)

    context = {'form': form}
    return render(request, 'editar_guardia.html', context)

def cargar_campaña(request):
    if request.method == 'POST':
        form = CampañaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Campaña cargada correctamente!")
            return redirect('Listar_campañas')
    else:
        form = CampañaForm()
        return render(request, 'cargar_campaña.html', {'form': form})
    
def editar_campaña(request, campaña_id):
    campaña = get_object_or_404(Campaña, id=campaña_id)

    if request.method == 'POST':
        form = CampañaForm(request.POST, instance=campaña)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Campaña editada correctamente!")
            return redirect('Listar_campañas')
    else:
        form = CampañaForm(instance=campaña)

    context = {'form': form}
    return render(request, 'editar_campaña.html', context)


def listar_campañas(request):
    campañas = Campaña.objects.all()
    context = {"campañas":paginar(request,campañas,6), "fechaHoy":datetime.datetime.today()}
    return render(request, 'listar_campañas.html', context)


def donar(request):
    sdk = mercadopago.SDK("TEST-2247251725354942-061914-a9d31ca1c16d102f5554d58738633dc0-1134118165")


 
    preference_data = {
        "items": [
            {
                "title": "Producto 1",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": 100.0
            }  
        ],
        "back_urls": {
        "success": "localhost:8000/",
        "failure": "localhost:8000/",
        "pending": "localhost:8000/"
    }
    }
    

    preference = sdk.preference().create(preference_data)

    payment_url = preference['response']['sandbox_init_point']
    print(payment_url)
    return redirect(payment_url)


