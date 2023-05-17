from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Turno
from email.mime.image import MIMEImage
from OhMyDog import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import os
import datetime
from django.utils import timezone
import schedule
import threading
import time
from pytz import timezone as tz

# Create your views here.

@login_required
def solicitar_turno(request):
    if request.method == 'POST':
        form = SolicitarTurnoForm(request.POST)
        if form.is_valid():
            cliente = request.user.cliente
            turno = form.save(commit=False)
            turno.cliente = cliente
            turno.estado_id = 3
            if Turno.objects.filter(cliente=cliente, fecha=form.cleaned_data['fecha']).exists():
                messages.error(request, 'Ya tiene un turno asignado para la fecha seleccionada.')
                return redirect('solicitar_turno')
            
            turno.save()

            messages.success(request, 'Turno solicitado correctamente.')
            return redirect('solicitar_turno')
    else:
        form = SolicitarTurnoForm()
    return render(request, 'solicitar_turno.html', {'form': form})

@login_required
def listar_turnos_pendientes(request):
    turnos = Turno.objects.filter(estado_id=3)
    return render(request, 'listar_pendientes.html', {'turnos': turnos})

def listar_turnos_confirmados(request):
    #turnos = Turno.objects.filter(estado_id=1)
    return render(request, 'listar_confirmados.html')#, {'turnos': turnos})

def listar_confirmados_del_dia(request):
    fecha_actual = date.today()
    turnos = Turno.objects.filter(estado_id=1, fecha=fecha_actual)
    return render(request, 'listar_confirmados_dia.html', {'turnos': turnos})



def run_scheduler():
    # Función que ejecuta el planificador en un bucle continuo
    while True:
        ("entra al run scheduler")
        schedule.run_pending()
        time.sleep(1)  # Pausa para evitar consumo excesivo de recursos


def enviar_recordatorio(turno):
    print("enviar recordatorio..")

    subject = 'Recordatorio de Turno'
    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = '%s' % (turno.cliente.user.email)
    reply_to_email = 'noreply@ejtechsoft.com'

    image_dir = os.path.join(settings.BASE_DIR, 'OhMyDogApp', 'static', 'OhMyDogApp', 'img')
    image_name = 'logo.png'

    context = {
        'nombre': turno.cliente.user.nombre,
        'fecha': turno.fecha.astimezone(tz('America/Argentina/Buenos_Aires')),
    }

    text_content = get_template('mail_recordatorio_turno.txt').render(context)
    html_content = get_template('mail_recordatorio_turno.html').render(context)

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


@login_required
def aceptar_solicitud(request, id_turno):
    turno = get_object_or_404(Turno, id=id_turno)

    hora_turno = request.POST.get('hora_turno')

    # Crear un objeto datetime con la fecha y hora seleccionadas
    fecha_hora_elegida = datetime.datetime.combine(turno.fecha.date(), datetime.datetime.strptime(hora_turno, '%H:%M').time())

    # Convertir la fecha y hora elegidas a la zona horaria configurada en Django
    fecha_hora_elegida = timezone.make_aware(fecha_hora_elegida, timezone.get_current_timezone())
    print("fecha hora elegida",fecha_hora_elegida)
    # Asignar la fecha y hora elegidas al turno
    turno.fecha = fecha_hora_elegida
    turno.estado_id = 1
    turno.save()


    subject = 'Solicitud de Turno Aceptada'
    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = '%s' % (turno.cliente.user.email)
    reply_to_email = 'noreply@ejtechsoft.com'

    image_dir = os.path.join(settings.BASE_DIR, 'OhMyDogApp', 'static', 'OhMyDogApp', 'img')
    image_name = 'logo.png'

    context = {
                'nombre' : turno.cliente.user.nombre,
                'fecha'  : turno.fecha.astimezone(tz('America/Argentina/Buenos_Aires')),
                }
    text_content = get_template('mail_confirmacion_turno.txt')
    html_content = get_template('mail_confirmacion_turno.html')
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

    # Obtener la fecha y hora del turno sin información de desplazamiento
    fecha_turno = turno.fecha.replace(tzinfo=None)

    # Obtener la fecha y hora actual en la zona horaria configurada en Django
    fecha_actual = timezone.localtime().replace(tzinfo=None)

    # Calculo de la fecha y hora del recordatorio (3 días antes del turno)
    fecha_recordatorio = fecha_turno - datetime.timedelta(days=3)

    # Calcular la diferencia de tiempo
    diferencia_tiempo = fecha_turno - fecha_actual
    print("fecha actual", fecha_actual)
    print("fecha recordatorio", fecha_recordatorio)
    print("diferencia de tiempo", diferencia_tiempo)
    # Verificar si todavía falta para el turno y la diferencia es mayor o igual a 3 días
    if (fecha_actual < fecha_turno) and (diferencia_tiempo >= datetime.timedelta(days=3)):
        print("ENTRÓ")
        schedule.every().day.at(fecha_recordatorio.strftime('%H:%M')).do(enviar_recordatorio, turno)

     # Ejecutar las tareas pendientes en el objeto `schedule.jobs`
    if not schedule.jobs:
        threading.Thread(target=run_scheduler, daemon=True).start()

    messages.success(request, 'Turno aceptado correctamente.')
    return redirect('/turnos/listar_turnos_pendientes/')

@login_required
def rechazar_solicitud(request, id_turno):
    turno = get_object_or_404(Turno, id=id_turno)
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        if not motivo:
            motivo = False

    subject = 'Solicitud de Turno Rechazada'
    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = '%s' % (turno.cliente.user.email)
    reply_to_email = 'noreply@ejtechsoft.com'

    image_dir = os.path.join(settings.BASE_DIR, 'OhMyDogApp', 'static', 'OhMyDogApp', 'img')
    image_name = 'logo.png'

    context = {
                'nombre' : turno.cliente.user.nombre,
                'atencion'  : turno.tipo_atencion.tipo,
                'fecha'  : turno.fecha.astimezone(tz('America/Argentina/Buenos_Aires')),
                'esVacuna' : 'Vacuna' in turno.tipo_atencion.tipo,
                'motivo' : motivo,
            }
    text_content = get_template('mail_turno_rechazado.txt')
    html_content = get_template('mail_turno_rechazado.html')
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
    
    
    turno.estado_id = 2
    turno.save()
    messages.success(request, 'Turno rechazado correctamente.')
    return redirect('/turnos/listar_turnos_pendientes/')
