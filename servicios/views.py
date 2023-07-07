from django.shortcuts import render
from .models import Personal
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
from unidecode import unidecode
from .models import Campaña
from .forms import DonacionForm
import mercadopago
from django.urls import reverse
from urllib.parse import urlparse
from django.db.models import F
from OhMyDog import settings
import tempfile
from django.core.mail import EmailMultiAlternatives
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from usuarios.models import Usuario

def listar_personal(request):
    personal = Personal.objects.all()
    filtros = {
        'tipo_consulta': request.GET.get('tipo-consulta'),
        'nombre_consulta': request.GET.get('nombre-consulta')
    }
    if any(value for value in filtros.values()):
        personal = buscar(request, filtros, personal)

    tipo_opciones = (
        ('paseador', 'Paseador'),
        ('cuidador', 'Cuidador'),
        ('guarderia', 'Guardería'),
    )
    contexto = {
        "personal":paginar(request,personal,6),
        "opciones_tipo": tipo_opciones,
    }
    return render(request, 'listar_personal.html', contexto)


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
        initial_values = {
            'nombre': campaña.nombre,
            'motivo': campaña.motivo,
            'objetivo': campaña.objetivo,
            'fechaInicio': campaña.fechaInicio.strftime('%Y-%m-%d'), 
            'fechaFin': campaña.fechaFin.strftime('%Y-%m-%d'), 
        }
        form = CampañaForm(initial=initial_values)

    context = {'form': form}
    return render(request, 'editar_campaña.html', context)


def listar_campañas(request):
    fechaHoy = datetime.datetime.today().date()
    campañas = Campaña.objects.filter(fechaFin__gt=fechaHoy)
    context = {"campañas": paginar(request, campañas, 6), "fechaHoy": fechaHoy}
    return render(request, 'listar_campañas.html', context)


def donar(request, campaña_id):
    campaña = get_object_or_404(Campaña, id=campaña_id)

    if request.method == 'POST':
        form = DonacionForm(request.POST, user=request.user)
        if form.is_valid():
            email = request.user.email if request.user.is_authenticated else form.cleaned_data['email']
            monto = request.POST.get('monto')
            preference_data = {
                "items": [
                    {
                        "title": campaña.nombre,
                        "quantity": 1,
                        "currency_id": "ARS",
                        "unit_price": float(monto)
                    }
                ],
                "back_urls": {
                    "success": request.build_absolute_uri(reverse('Donacion_exitosa', args=[campaña_id, monto]) + f'?email={email}'),
                    "failure": request.build_absolute_uri(reverse('Donar', args=[campaña_id])),
                    "pending": request.build_absolute_uri(reverse('Donar', args=[campaña_id]))
                }
            }
            sdk = mercadopago.SDK("TEST-2247251725354942-061914-a9d31ca1c16d102f5554d58738633dc0-1134118165")
            preference = sdk.preference().create(preference_data)
            payment_url = preference['response']['sandbox_init_point']
            return redirect(payment_url)
    else:
        form = DonacionForm()

    return render(request, 'donar.html', {'form': form, 'campaña': campaña})


def donacion_exitosa(request, campaña_id, monto):
    campaña = get_object_or_404(Campaña, id=campaña_id)

    email = request.GET.get('email', '')

    campaña.recaudado = F('recaudado') + int(monto)
    campaña.save()

    donacion = Donacion.objects.create(
        campaña=campaña,
        monto=int(monto),
        fecha=datetime.datetime.now(),
        nombre=request.user.nombre if request.user.is_authenticated else None,
        apellido=request.user.apellido if request.user.is_authenticated else None,
        email=request.user.email if request.user.is_authenticated else email,
    )

    subject = 'Donación Exitosa'
    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = request.user.email if request.user.is_authenticated else email
    reply_to_email = 'noreply@ejtechsoft.com'


    context = {
        'nombre_donador': request.user.nombre if request.user.is_authenticated else None,
        'apellido_donador': request.user.apellido if request.user.is_authenticated else None,
        'email_donador': request.user.email if request.user.is_authenticated else email,
        'campaña': campaña.nombre,
        'monto': monto,
        'fecha': donacion.fecha,
    }

    text_content = get_template('mail/donacion_mail.txt')
    html_content = get_template('mail/donacion_mail.html')
    text_content = text_content.render(context)
    html_content = html_content.render(context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
    email.mixed_subtype = 'related'
    email.content_subtype = 'html'
    email.attach_alternative(html_content, 'text/html')

    html_content = get_template('mail/comprobante_donacion.html')
    html_content = html_content.render(context)
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        if not pisa_status.err:
            pdf_file.seek(0)
            email.attach('comprobante_donacion.pdf', pdf_file.read(), 'application/pdf')

    
    email.send(fail_silently=False)
    
    if request.user.is_authenticated:
        request.user.descuento = True
        request.user.save()
        return redirect('Listar_donaciones')
    elif Usuario.objects.filter(email = to_email):
        user = Usuario.objects.get(email=to_email)
        user.descuento = True
        user.save()
        
    return redirect('Listar_campañas')
    


def listar_donaciones(request):
    donaciones = Donacion.objects.filter(email=request.user.email)
    context = {"donaciones": paginar(request, donaciones, 6)}
    return render(request, 'listar_donaciones.html', context)


def descargar_comprobante(request, donacion_id):
    donacion = get_object_or_404(Donacion, id=donacion_id)

    context = {
        'nombre_donador': donacion.nombre,
        'apellido_donador': donacion.apellido,
        'email_donador': donacion.email,
        'campaña': donacion.campaña.nombre,
        'monto': donacion.monto,
        'fecha': donacion.fecha,
    }

    html_content = get_template('mail/comprobante_donacion.html')
    html_content = html_content.render(context)
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        if not pisa_status.err:
            pdf_file.seek(0)
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=comprobante_donacion.pdf'
            return response

    return redirect('Listar_donaciones')

def buscar(request, filtros, personal):
    print("FILTRO",filtros)

    personal_filtrados = personal

    if filtros['tipo_consulta']:
        consulta = filtros['tipo_consulta']
        personal_filtrados = personal_filtrados.filter(tipo=consulta)
    
    if filtros['nombre_consulta']:
        consulta = filtros['nombre_consulta']
        personal_filtrados = personal_filtrados.filter(nombre__icontains=unidecode(consulta))
        
    if  not personal_filtrados:
        messages.add_message(request, messages.ERROR, 'No hay turnos para la búsqueda realizada')
        personal_filtrados = personal

    return personal_filtrados