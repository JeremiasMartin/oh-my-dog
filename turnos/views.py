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
    return render(request, 'listar_turnos.html', {'turnos': turnos})



def enviar_recordatorio(turno):
    # Calcular la fecha del recordatorio (3 días antes de la fecha del turno)
    fecha_recordatorio = turno.fecha - datetime.timedelta(days=1)

    # Comprobar si el la fecha_recordatorio ya pasó o la fecha del turno es antes de que transcurran 3 días (por lo tanto no envíar mail de recordatorio)
    if (timezone.now() >= fecha_recordatorio) or (timezone.now() >= turno.fecha - datetime.timedelta(days=1)):
        return

    subject = 'Recordatorio de Turno'
    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = '%s' % (turno.cliente.user.email)
    reply_to_email = 'noreply@ejtechsoft.com'

    image_dir = os.path.join(settings.BASE_DIR, 'OhMyDogApp', 'static', 'OhMyDogApp', 'img')
    image_name = 'logo.png'

    context = {
        'nombre': turno.cliente.nombre,
        'fecha': turno.fecha,
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
    turno.estado_id = 1
    turno.save()


    subject = 'Solicitud de Turno Aceptada'
    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = '%s' % (turno.cliente.user.email)
    reply_to_email = 'noreply@ejtechsoft.com'

    image_dir = os.path.join(settings.BASE_DIR, 'OhMyDogApp', 'static', 'OhMyDogApp', 'img')
    image_name = 'logo.png'

    context = {
                'nombre' : turno.cliente.nombre,
                'fecha'  : turno.fecha
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
    # Programar correo de recordatorio 3 días antes del turno
    fecha_recordatorio = turno.fecha - datetime.timedelta(days=1)
    fecha_recordatorio_aware = timezone.make_aware(datetime.datetime.combine(fecha_recordatorio, datetime.time(hour=9)))
    if (timezone.now().date() < fecha_recordatorio) and ((turno.fecha - timezone.now().date()) >= datetime.timedelta(days=1)):
        schedule.every().day.at(fecha_recordatorio_aware.strftime('%H:%M')).do(enviar_recordatorio, turno)
     # Ejecutar las tareas pendientes en el objeto `schedule.jobs`
    for job in schedule.jobs:
        job.run()
    messages.success(request, 'Turno aceptado correctamente.')
    return redirect('/turnos/listar_turnos_pendientes/')

@login_required
def rechazar_solicitud(request, id_turno):
    turno = get_object_or_404(Turno, id=id_turno)
    turno.estado_id = 2
    turno.save()
    messages.success(request, 'Turno rechazado correctamente.')
    return redirect('/turnos/listar_turnos_pendientes/')
