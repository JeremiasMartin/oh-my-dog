from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from turnos.views import paginar
from .forms import CruzaForm
from publicaciones.models import Perro_publicacion, Publicacion
from .models import Postulacion
from django.db.models import Q
from OhMyDog import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

def listar_mis_mascotas_cruza(request):
    mascotas = Publicacion.objects.filter(tipo_publicacion="Cruza", id_usuario=request.user.id)
    for publicacion in mascotas:
        publicacion.id_perro_publicacion.edad = calcular_edad(publicacion.id)
    contexto = {
        "cruzas":paginar(request, mascotas, 3),
    }
    return render(request, 'mis_mascotas_cruza.html', contexto)

def registrar_mascota_cruza(request):
    if request.method == 'POST':
        form = CruzaForm(request.POST, request.FILES)
        if form.is_valid():
            perro_publicacion = Perro_publicacion(
                nombre=form.cleaned_data.get('nombre'),
                tamanio=form.cleaned_data.get('tamanio'),
                sexo=form.cleaned_data.get('sexo'),
                color=form.cleaned_data.get('color'),
                edad=form.cleaned_data.get('edad'),
                raza=form.cleaned_data.get('raza'),
                foto=request.FILES.get('foto')
            )
            perro_publicacion.save()

            if (perro_publicacion.sexo == 'H'):
                periodo_celo=form.cleaned_data.get('periodo_celo')
            else:
                periodo_celo=None

            publicacion = Publicacion(
                descripcion=periodo_celo,
                id_usuario=request.user,
                id_perro_publicacion=perro_publicacion,
                activo=True,
                tipo_publicacion = "Cruza",
            )
            publicacion.save()

            messages.success(request, 'Registro exitoso')
            return redirect('Mis_mascotas_cruza')
        else:
            messages.error(request, 'Debe completar todos los campos')
    else:
        form = CruzaForm()
        
    return render(request, 'registrar_mascota_cruza.html', {'form': form})

def editar_perfil_mascota_cruza(request, id_publicacion):
    publicacion = get_object_or_404(Publicacion, id=id_publicacion)
    perro_publicacion = get_object_or_404(Perro_publicacion, id=publicacion.id_perro_publicacion_id)
    perro_publicacion.edad = calcular_edad(id_publicacion)

    if request.method == 'POST':
        form = CruzaForm(request.POST, request.FILES)
        if form.is_valid() or 'foto' not in request.FILES:
            perro_publicacion.nombre = form.cleaned_data.get('nombre')
            perro_publicacion.tamanio = form.cleaned_data.get('tamanio')
            perro_publicacion.sexo = form.cleaned_data.get('sexo')
            perro_publicacion.color = form.cleaned_data.get('color')
            perro_publicacion.edad = form.cleaned_data.get('edad')
            perro_publicacion.raza = form.cleaned_data.get('raza')
            foto = form.cleaned_data.get('foto')
            if foto:
                perro_publicacion.foto = foto
            perro_publicacion.save()
            if (perro_publicacion.sexo == 'H'):
                periodo_celo=form.cleaned_data.get('periodo_celo')
            else:
                periodo_celo=None

            publicacion.descripcion = periodo_celo
            publicacion.fecha_ultima_modificacion = datetime.now()
            publicacion.save()

            messages.success(request, "¡Información actualizada correctamente!")
            return redirect('Mis_mascotas_cruza')
    else:
        form = CruzaForm(initial={
            'nombre': perro_publicacion.nombre,
            'tamanio': perro_publicacion.tamanio,
            'sexo': perro_publicacion.sexo,
            'color': perro_publicacion.color,
            'edad': perro_publicacion.edad,
            'raza': perro_publicacion.raza,
            'foto': perro_publicacion.foto,
            'periodo_celo': publicacion.descripcion,
        })
    return render(request, 'editar_mascota_cruza.html', {'form': form})

def cambiar_estado_publicacion(id_publicacion):
    publicacion = get_object_or_404(Publicacion,id=id_publicacion)
    if(publicacion.activo):
        publicacion.activo = False
    else:
        publicacion.activo = True
    publicacion.save()

    return redirect('Mis_mascotas_cruza')

def postularse_mascota_cruza(request, publicacion_a_postular, postulante):
    postulacion_previa = Postulacion.objects.filter(publicacion=postulante, publicacion_postulante=publicacion_a_postular).first()
    publicacion = get_object_or_404(Publicacion, id=publicacion_a_postular)
    publicacion_postulante = get_object_or_404(Publicacion, id=postulante)
    
    postulacion = Postulacion.objects.create(
        publicacion = publicacion,
        publicacion_postulante = publicacion_postulante,
    )

    if postulacion_previa:
        postulacion.match = True
        postulacion_previa.match = True
        postulacion.fecha_match = datetime.now()
        postulacion_previa.fecha_match = datetime.now()
        postulacion.save()
        postulacion_previa.save()
        messages.success(request, 'Hay coincidencia, se envió un mail con los datos para ponerse en contacto')
        enviar_mail_match(publicacion_match=publicacion_postulante, publicacion_anterior=publicacion)
    else:
        messages.success(request, 'Postulación exitosa')
    
    return redirect('Recomendados', id_publicacion=postulante)
    
def listar_recomendados(request, id_publicacion):
    publicacion=get_object_or_404(Publicacion, id=id_publicacion)
    raza=publicacion.id_perro_publicacion.raza
    edad=calcular_edad(id_publicacion)

    #Obtengo las distintas publicaciones
    postulados = postulantes(id_publicacion=id_publicacion, match=False)
    postulaciones = mis_postulaciones(id_publicacion)
    match = postulantes(id_publicacion=id_publicacion, match=True)
    no_postulados = Publicacion.objects.filter(tipo_publicacion="Cruza", activo=True) \
        .exclude(Q(id_perro_publicacion__sexo=publicacion.id_perro_publicacion.sexo) |
                 Q(id_usuario=publicacion.id_usuario) |
                 Q(id__in=postulados.values_list('id', flat=True)) |
                 Q(id__in=postulaciones.values_list('id', flat=True)) |
                 Q(id__in=match.values_list('id', flat=True)))
    #Ordeno publicaciones que se pueden postular
    postulados_ordenados = ordenar_raza_edad(postulados, raza, edad)
    no_postulados_ordenados = ordenar_raza_edad(no_postulados, raza, edad)
    #Identifico cada publicacion con el tipo de recomendado
    recomendados = agregar_tipo_a_lista(postulados_ordenados, 'postulados') + \
                   agregar_tipo_a_lista(no_postulados_ordenados, 'no_postulados') + \
                   agregar_tipo_a_lista(postulaciones, 'postulaciones') + \
                   agregar_tipo_a_lista(match, 'match')
    #Calcula la edad real al dia de la fecha
    for recomendado in recomendados:
        recomendado['publicacion'].id_perro_publicacion.edad = calcular_edad(recomendado['publicacion'].id)
    
    context={
        'recomendados': paginar(request, recomendados, 3),
        'publicacion': publicacion,
    }
    return render(request, 'listar_recomendados.html', context)

def postulantes(id_publicacion, match=False):
    postulaciones = Postulacion.objects.filter(publicacion=id_publicacion, match=match)
    postulacion_ids = postulaciones.values_list('publicacion_postulante__id', flat=True)
    publicaciones = Publicacion.objects.filter(id__in=postulacion_ids)
    return publicaciones

def mis_postulaciones(id_publicacion):
    postulaciones=Postulacion.objects.filter(publicacion_postulante=id_publicacion, match=False)
    postulacion_ids = postulaciones.values_list('publicacion__id', flat=True)
    publicaciones = Publicacion.objects.filter(id__in=postulacion_ids)
    return publicaciones

def ordenar_raza_edad(publicaciones, raza, edad):
    misma_raza = publicaciones.filter(id_perro_publicacion__raza__icontains=raza)
    misma_raza = ordenar_edad(misma_raza, edad)

    diferente_raza = publicaciones.filter(~Q(id_perro_publicacion__raza__icontains=raza))
    diferente_raza = ordenar_edad(diferente_raza, edad)

    return list(misma_raza) + list(diferente_raza)

def ordenar_edad(publicaciones, edad):
    print("ANTES DEL ANOTATE")
    ordenadas = sorted(publicaciones, key=lambda p: distancia_edad(p.id, edad))
    print(ordenadas)
    print("DESPUES DEL ANOTATE")
    return ordenadas

def agregar_tipo_a_lista(publicaciones,tipo):
    return [{'publicacion': publicacion, 'tipo': tipo} for publicacion in publicaciones]

def enviar_mail_match(publicacion_match, publicacion_anterior):
    enviar_mail_postulante(publicacion_a_postular=publicacion_anterior, publicacion_postulante=publicacion_match)
    enviar_mail_postulante(publicacion_a_postular=publicacion_match, publicacion_postulante=publicacion_anterior)

def enviar_mail_postulante(publicacion_a_postular, publicacion_postulante):
    subject = '¡Coincidencia encontrada! Una gran oportunidad para la cruza de perros'
    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = publicacion_a_postular.id_usuario.email
    reply_to_email = 'noreply@ejtechsoft.com'
    
    context = {
        'owner': publicacion_a_postular.id_usuario.nombre,
        'mascota': publicacion_a_postular.id_perro_publicacion.nombre,
        'interesado' : publicacion_postulante.id_usuario,
        'mascota_interesada' : publicacion_postulante.id_perro_publicacion,
        'edad': calcular_edad_string(calcular_edad(publicacion_postulante.id))
    }

    text_content = get_template('mail/postulacion_cruza_mail.txt')
    html_content = get_template('mail/postulacion_cruza_mail.html')
    text_content = text_content.render(context)
    html_content = html_content.render(context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
    email.mixed_subtype = 'related'
    email.content_subtype = 'html'
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=False)

def calcular_edad_string(edad):
    edad_meses = int(edad)
    if (edad_meses == 1):
        return str(edad_meses) + " mes"
    elif (edad_meses > 11):
        edad_años = edad_meses // 12
        if (edad_años == 1):
            return str(edad_años) + " año"
        else:
            return str(edad_años) + " años"
    else:
        return str(edad_meses) + " meses"
    
def calcular_edad(id_publicacion):
    fecha_hoy = datetime.now().date()
    publicacion = Publicacion.objects.get(id=id_publicacion)
    fecha_modificacion = publicacion.fecha_ultima_modificacion
    meses_transcurridos = (
            (fecha_hoy.year - fecha_modificacion.year) * 12
            + (fecha_hoy.month - fecha_modificacion.month)
        )
    edad = meses_transcurridos + int(publicacion.id_perro_publicacion.edad)
    print("EDAD", edad)
    return str(edad)

def distancia_edad(id_publicacion, edad):
    return abs((int(calcular_edad(id_publicacion)) - int(edad)))