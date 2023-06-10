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
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.db.models import Q,Value as V, Func, F
from unidecode import unidecode


# Create your views here.

@login_required
def solicitar_turno(request):
    cliente = request.user.cliente
    if request.method == 'POST':
        form = SolicitarTurnoForm(cliente, request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.cliente = cliente
            turno.estado_id = 3

            if Turno.objects.filter(cliente=cliente, fecha=form.cleaned_data['fecha']).exists():
                messages.error(request, 'Ya tiene un turno solicitado para la fecha seleccionada.')
                return redirect('solicitar_turno')
            
            turno.save()

            messages.success(request, 'Turno solicitado correctamente.')
            return redirect('solicitar_turno')
        else:
            print('FORM NOT VALID')
            print("Form errors:", form.errors)
    else:
        form = SolicitarTurnoForm(cliente=cliente)

    return render(request, 'solicitar_turno.html', {'form': form})

@login_required
def listar_turnos_pendientes(request):
    turnos = Turno.objects.filter(estado_id=3)
    filtros = {
        'fecha_consulta': request.GET.get('fecha-consulta'),
        'atencion_consulta': request.GET.get('atencion-consulta'),
        'dni_consulta': request.GET.get('dni-consulta'),
        'nombre_apellido_consulta': request.GET.get('nombre_apellido-consulta')
    }
    if any(value for value in filtros.values()):
        turnos = buscar(request, filtros, turnos)

    return render(request, 'listar_pendientes.html', {'turnos': paginar(request, turnos, 6)})

def listar_turnos_confirmados(request):
    turnos = Turno.objects.filter(estado_id=1)
    filtros = {
        'fecha_consulta': request.GET.get('fecha-consulta'),
        'atencion_consulta': request.GET.get('atencion-consulta'),
        'dni_consulta': request.GET.get('dni-consulta'),
        'nombre_apellido_consulta': request.GET.get('nombre_apellido-consulta')
    }
    if any(value for value in filtros.values()):
        turnos = buscar(request, filtros, turnos)

    return render(request, 'listar_confirmados.html', {'turnos': paginar(request, turnos, 6)})

def listar_confirmados_del_dia(request):
    fecha_actual = timezone.localtime().date()
    turnos = Turno.objects.filter(estado_id=1, fecha__date=fecha_actual)
    filtros = {
        'fecha_consulta': request.GET.get('fecha-consulta'),
        'atencion_consulta': request.GET.get('atencion-consulta'),
        'dni_consulta': request.GET.get('dni-consulta'),
        'nombre_apellido_consulta': request.GET.get('nombre_apellido-consulta')
    }
    if any(value for value in filtros.values()):
        turnos = buscar(request, filtros, turnos)
        
    return render(request, 'listar_confirmados.html', {'turnos': paginar(request, turnos, 6)})


def run_scheduler():
    # Función que ejecuta el planificador en un bucle continuo
    while True:
        ("entra al run scheduler")
        schedule.run_pending()
        time.sleep(1)  # Pausa para evitar consumo excesivo de recursos


def enviar_recordatorio(turno, fecha_turno):
    print("enviar recordatorio..")
    fecha_actual = timezone.localtime().replace(tzinfo=None).replace(second=0, microsecond=0)
    fecha_recordatorio = fecha_turno - datetime.timedelta(days=3)
    fecha_recordatorio = fecha_recordatorio.replace(second=0)
    print("fecha actual", fecha_actual)
    print("fecha recordatorio", fecha_recordatorio)
    if fecha_actual != fecha_recordatorio:
        return
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
    # print("fecha actual", fecha_actual)
    # print("fecha recordatorio", fecha_recordatorio)
    # print("diferencia de tiempo", diferencia_tiempo)
    # Verificar si todavía falta para el turno y la diferencia es mayor o igual a 3 días
    if (fecha_actual < fecha_turno) and (diferencia_tiempo >= datetime.timedelta(days=3)):
        print("ENTRÓ")
        schedule.every().day.at(fecha_recordatorio.strftime('%H:%M')).do(enviar_recordatorio, turno, fecha_turno)
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
        if motivo:
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


def buscar(request, filtros, turnos):
    print("FILTRO",filtros)

    turnos_filtrados = turnos

    if filtros['fecha_consulta']:
        consulta = filtros['fecha_consulta']
        turnos_filtrados = turnos_filtrados.filter(fecha__date=consulta)
    
    if filtros['atencion_consulta']:
        consulta = unidecode(filtros['atencion_consulta'])
        turnos_filtrados = turnos_filtrados.annotate(tipo_without_accents=Func(F('tipo_atencion__tipo'), function='unaccent')).\
                filter(tipo_without_accents__icontains=consulta)
    
    if filtros['dni_consulta']:
        consulta = filtros['dni_consulta']
        turnos_filtrados = turnos_filtrados.filter(cliente__user__dni__icontains=consulta)
    
    if filtros['nombre_apellido_consulta']:
        consulta = filtros['nombre_apellido_consulta']
        turnos_filtrados = turnos_filtrados.annotate(nombre_completo=Concat('cliente__user__nombre', V(' '), 'cliente__user__apellido')).\
                filter(
                    Q(nombre_completo__icontains=unidecode(consulta)) |
                    Q(nombre_completo__icontains=unidecode(" ".join(reversed(consulta.split()))))
                )
        
    if  not turnos_filtrados:
        messages.add_message(request, messages.ERROR, 'No hay turnos para la búsqueda realizada')
        turnos_filtrados = turnos

    return turnos_filtrados


def paginar(request,elementos, cantidad):
    paginator = Paginator(elementos,cantidad)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj