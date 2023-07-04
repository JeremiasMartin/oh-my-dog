from django.shortcuts import render, redirect
from .forms import AdopcionForm, PostulacionForm, EditarAdopcionForm, PublicarPerroPerdidoForm, CargarPerroEncontradoForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from OhMyDog import settings
from django.core.mail import EmailMultiAlternatives
import xhtml2pdf.pisa as pisa
import tempfile
import datetime
from turnos.views import paginar
from unidecode import unidecode
from django.db.models.functions import Concat
from django.db.models import Q, Value as V

from django.shortcuts import render, redirect
from django.contrib import messages

def publicar_adopcion(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST, request.FILES)
        if form.is_valid():
            perro_nombre = form.cleaned_data.get('nombre')
            if perro_nombre is not None and perro_nombre.strip() == '':
                perro_nombre = None  # Si el nombre está vacío, se establece como None

            perro_publicacion = Perro_publicacion(
                nombre=perro_nombre,
                tamanio=form.cleaned_data.get('tamanio'),
                sexo=form.cleaned_data.get('sexo'),
                color=form.cleaned_data.get('color'),
                edad=form.cleaned_data.get('edad'),
                raza=form.cleaned_data.get('raza'),
            )
            perro_publicacion.save()

            publicacion = Publicacion(
                descripcion=form.cleaned_data.get('motivo_adopcion'),
                id_usuario=request.user,
                id_perro_publicacion=perro_publicacion,
                activo=True,
                tipo_publicacion = 'Adopcion',
            )
            publicacion.save()

            adopcion = Adopcion(
                id_publicacion=publicacion,
                motivo_adopcion=form.cleaned_data.get('motivo_adopcion'),
                origen=form.cleaned_data.get('origen'),
            )
            adopcion.save()

            messages.success(request, 'Publicación exitosa')
            return redirect('listar_mis_publicaciones_adopcion')
        else:
            messages.error(request, 'Debe completar todos los campos')
    else:
        form = AdopcionForm()
        
    return render(request, 'publicar_adopcion.html', {'form': form})


@login_required
def listar_mis_publicaciones_adopcion(request):
    adopciones = Adopcion.objects.filter(id_publicacion__id_usuario=request.user.id).order_by('-id')
    
    filtros = {
        'raza_consulta': request.GET.get('raza-consulta'),
        'sexo_consulta': request.GET.get('sexo-consulta'),
        'tamanio_consulta': request.GET.get('tamanio-consulta'),
    }
    if any(value for value in filtros.values()):
        adopciones = buscar_mascotas(request, filtros, adopciones)

    tamanio_opciones = (
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    )
    sexo_opciones = (
        ('M', 'Macho'),
        ('H', 'Hembra')
    )
    contexto = {
        "adopciones":paginar(request, adopciones, 3),
        "opciones_tamanios": tamanio_opciones,
        'opciones_sexo': sexo_opciones
    }
    return render(request, 'listar_mis_publicaciones_adopcion.html', contexto)
    

def listar_adopciones(request):
    adopciones = Adopcion.objects.all().order_by('-id')
    
    filtros = {
        'raza_consulta': request.GET.get('raza-consulta'),
        'sexo_consulta': request.GET.get('sexo-consulta'),
        'tamanio_consulta': request.GET.get('tamanio-consulta'),
    }
    if any(value for value in filtros.values()):
        adopciones = buscar_mascotas(request, filtros, adopciones)

    tamanio_opciones = (
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    )
    sexo_opciones = (
        ('M', 'Macho'),
        ('H', 'Hembra')
    )
    contexto = {
        "adopciones":paginar(request, adopciones, 3),
        "opciones_tamanios": tamanio_opciones,
        'opciones_sexo': sexo_opciones
    }
    return render(request, 'listar_adopciones.html',  contexto)


def postularse(request, adopcion_id):
    adopcion = get_object_or_404(Adopcion, id=adopcion_id)
    esRegistrado = request.user.is_authenticated
    if esRegistrado:
        perfil = request.user
        if Postulacion.objects.filter(publicacion_adopcion=adopcion, email=request.user.email).exists():
            messages.error(request, 'Ya te has postulado para esta mascota.')
            return redirect('listar_postulaciones_adopcion')
    else:
        email_postulante = request.POST.get('email')

        if adopcion.id_publicacion.id_usuario.email == email_postulante:
            messages.error(request, 'No puedes postularte para tu propia publicación.')
            return redirect('postularse', adopcion_id=adopcion_id)

        if Postulacion.objects.filter(publicacion_adopcion=adopcion, email=email_postulante).exists():
            messages.error(request, 'Ya te has postulado para esta mascota.')
            return redirect('postularse', adopcion_id=adopcion_id)

    if request.method == 'POST':
        form = PostulacionForm(request.POST, esRegistrado=esRegistrado)
        print(form.errors)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.publicacion_adopcion = adopcion

            if esRegistrado:
                postulacion.nombre = perfil.nombre
                postulacion.apellido = perfil.apellido
                postulacion.email = perfil.email
                postulacion.telefono = perfil.telefono

            postulacion.save()

            subject = 'Postulación Exitosa'
            from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
            to_email = postulacion.email if esRegistrado else form.cleaned_data.get('email')
            reply_to_email = 'noreply@ejtechsoft.com'

            nombre_postulante = postulacion.nombre if esRegistrado else form.cleaned_data.get('nombre')

            context = {
                'nombre_postulante': nombre_postulante,
                'nombre_mascota': postulacion.publicacion_adopcion.id_publicacion.id_perro_publicacion.nombre,
            }

            text_content = get_template('mail/postulacion_mail.txt')
            html_content = get_template('mail/postulacion_mail.html')
            text_content = text_content.render(context)
            html_content = html_content.render(context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
            email.mixed_subtype = 'related'
            email.content_subtype = 'html'
            email.attach_alternative(html_content, 'text/html')
            email.send(fail_silently=False)
            enviar_postulante_a_publicador(postulacion, form.cleaned_data.get('mensaje'))
            messages.success(request, 'Postulación enviada')
            if(esRegistrado):
                 return redirect('listar_postulaciones_adopcion')
            else:
                return redirect('listar_adopciones')

    else:
        form = PostulacionForm()
    return render(request, 'postularse.html', {'form': form, 'adopcion_id': adopcion_id, 'esRegistrado': esRegistrado})



def enviar_postulante_a_publicador(postulacion, mensaje):
    subject = f"Nuevo postulante"
    if postulacion.publicacion_adopcion.id_publicacion.id_perro_publicacion.nombre:
        subject += f" de {postulacion.publicacion_adopcion.id_publicacion.id_perro_publicacion.nombre}"

    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = '%s' % (postulacion.publicacion_adopcion.id_publicacion.id_usuario.email)
    reply_to_email = 'noreply@ejtechsoft.com'
    context = {
                    'nombre_publicador' : postulacion.publicacion_adopcion.id_publicacion.id_usuario.nombre,
                    'nombre_postulante' : postulacion.nombre,
                    'apellido_postulante' : postulacion.apellido,
                    'telefono_postulante' : postulacion.telefono,
                    'email_postulante' : postulacion.email,
                    'motivo_postulante' : mensaje,
                    'nombre_mascota'  : postulacion.publicacion_adopcion.id_publicacion.id_perro_publicacion.nombre,
                    }
    text_content = get_template('mail/datos_postulante.txt')
    html_content = get_template('mail/datos_postulante.html')
    text_content = text_content.render(context)
    html_content = html_content.render(context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
    email.mixed_subtype = 'related'
    email.content_subtype = 'html'
    email.attach_alternative(html_content, 'text/html')

    email.send(fail_silently=False)


def listar_postulantes_adopcion(request, adopcion_id):
    postulantes = Postulacion.objects.filter(publicacion_adopcion_id=adopcion_id)
    consulta = request.GET.get('consulta', None)
    if consulta:
        postulantes = buscar_postulantes(request, consulta, postulantes)

    tiene_adoptante = False
    adoptante_seleccionado = None
    publicacion = Adopcion.objects.filter(id=adopcion_id, adoptante__isnull=False).first()
    if publicacion:
        tiene_adoptante = True
        adoptante_seleccionado = publicacion.adoptante
    
    return render(request, 'listar_postulantes_adopcion.html', {'postulantes': paginar(request, postulantes, 6), 'tiene_adoptante': tiene_adoptante, 'adoptante_seleccionado': adoptante_seleccionado})

def seleccionar_postulante_adopcion(request, postulante_id):
    postulante = Postulacion.objects.get(id=postulante_id)
    adopcion = postulante.publicacion_adopcion
    adopcion.id_publicacion.activo = False
    adopcion.adoptante = postulante
    adopcion.id_publicacion.save()
    adopcion.save()
    enviar_seleccionado_adopcion(postulante)
    return redirect('listar_adopciones')

def enviar_seleccionado_adopcion(postulante):
    subject = f"Postulante seleccionado"
    if postulante.publicacion_adopcion.id_publicacion.id_perro_publicacion.nombre:
        subject += f" de {postulante.publicacion_adopcion.id_publicacion.id_perro_publicacion.nombre}"

    from_email = 'Ejtech <%s>' % (settings.EMAIL_HOST_USER)
    to_email = '%s' % (postulante.email)
    reply_to_email = 'noreply@ejtechsoft.com'
    context = {
                    'nombre_postulante' : postulante.nombre,
                    'apellido_postulante' : postulante.apellido,
                    'telefono_postulante' : postulante.telefono,
                    'email_postulante' : postulante.email,
                    'telefono_publicador' : postulante.publicacion_adopcion.id_publicacion.id_usuario.telefono,
                    'nombre_mascota'  : postulante.publicacion_adopcion.id_publicacion.id_perro_publicacion.nombre,
                    'email_publicador' : postulante.publicacion_adopcion.id_publicacion.id_usuario.email,
                    'nombre_publicador' : postulante.publicacion_adopcion.id_publicacion.id_usuario.nombre,
                    'apellido_publicador' : postulante.publicacion_adopcion.id_publicacion.id_usuario.apellido,
                    'fecha_adopcion' : datetime.datetime.now().strftime("%d/%m/%Y"),
    }
    text_content = get_template('mail/postulante_seleccionado.txt')
    html_content = get_template('mail/postulante_seleccionado.html')
    text_content = text_content.render(context)
    html_content = html_content.render(context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
    email.mixed_subtype = 'related'
    email.content_subtype = 'html'
    email.attach_alternative(html_content, 'text/html')



    html_content = get_template('mail/comprobante_adopcion.html')
    html_content = html_content.render(context)
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        if not pisa_status.err:
            pdf_file.seek(0)
            email.attach('comprobante_adopcion.pdf', pdf_file.read(), 'application/pdf')

    email.send(fail_silently=False)

def listar_mis_postulaciones(request):
    postulaciones = Postulacion.objects.filter(email=request.user.email)
    print(postulaciones)
    filtros = {
        'raza_consulta': request.GET.get('raza-consulta'),
        'sexo_consulta': request.GET.get('sexo-consulta'),
        'tamanio_consulta': request.GET.get('tamanio-consulta'),
    }
    if any(value for value in filtros.values()):
        postulaciones = buscar_postulaciones(request, filtros, postulaciones)

    tamanio_opciones = (
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    )
    sexo_opciones = (
        ('M', 'Macho'),
        ('H', 'Hembra')
    )
    contexto = {
        "postulaciones":paginar(request, postulaciones, 3),
        "opciones_tamanios": tamanio_opciones,
        'opciones_sexo': sexo_opciones
    }
    return render(request, 'listar_mis_postulaciones.html', contexto)

def buscar_postulaciones(request, filtros, postulaciones):
    postulaciones_filtradas = postulaciones
    
    if filtros['raza_consulta']:
        consulta = filtros['raza_consulta']
        postulaciones_filtradas = postulaciones_filtradas.filter(publicacion_adopcion__id_publicacion__id_perro_publicacion__raza__icontains=unidecode(consulta))
        
    if filtros['sexo_consulta']:
        consulta = filtros['sexo_consulta']
        postulaciones_filtradas = postulaciones_filtradas.filter(publicacion_adopcion__id_publicacion__id_perro_publicacion__sexo=consulta)
    
    if filtros['tamanio_consulta']:
        consulta = filtros['tamanio_consulta']
        postulaciones_filtradas = postulaciones_filtradas.filter(publicacion_adopcion__id_publicacion__id_perro_publicacion__tamanio=consulta)
    
    if  not postulaciones_filtradas:
        messages.add_message(request, messages.ERROR, 'No se encontraron resultados para la búsqueda')
        postulaciones_filtradas = postulaciones

    return postulaciones_filtradas



def buscar_mascotas(request, filtros, adopciones):
    print("FILTRO",filtros)
    adopciones_filtradas = adopciones
    
    if filtros['raza_consulta']:
        consulta = filtros['raza_consulta']
        adopciones_filtradas = adopciones_filtradas.filter(id_publicacion__id_perro_publicacion__raza__icontains=unidecode(consulta))
        
    if filtros['sexo_consulta']:
        consulta = filtros['sexo_consulta']
        adopciones_filtradas = adopciones_filtradas.filter(id_publicacion__id_perro_publicacion__sexo=consulta)
    
    if filtros['tamanio_consulta']:
        consulta = filtros['tamanio_consulta']
        adopciones_filtradas = adopciones_filtradas.filter(id_publicacion__id_perro_publicacion__tamanio=consulta)
    
    if  not adopciones_filtradas:
        messages.add_message(request, messages.ERROR, 'No hay perros para la búsqueda realizada')
        adopciones_filtradas = adopciones

    return adopciones_filtradas

def buscar_postulantes(request, consulta, postulantes):
    print("CONSULTA",consulta)
    
    postulantes_filtrados = postulantes.annotate(nombre_completo=Concat('nombre', V(' '), 'apellido')).\
                filter(
                    Q(nombre_completo__icontains=unidecode(consulta)) |
                    Q(nombre_completo__icontains=unidecode(" ".join(reversed(consulta.split()))))
                )
    
    if  not postulantes_filtrados:
        messages.add_message(request, messages.ERROR, 'No hay postulantes para la búsqueda realizada')
        postulantes_filtrados = postulantes

    return postulantes_filtrados

def editar_adopcion(request, adopcion_id):
    adopcion = get_object_or_404(Adopcion, id=adopcion_id)
    publicacion = get_object_or_404(Publicacion, id=adopcion.id_publicacion_id)
    perro_publicacion = get_object_or_404(Perro_publicacion, id=publicacion.id_perro_publicacion_id)

    path_anterior = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = EditarAdopcionForm(request.POST or None)
        if form.is_valid():
            path_anterior = request.POST.get('path_anterior', '/')

            perro_publicacion.nombre = form.cleaned_data.get('nombre')
            perro_publicacion.tamanio = form.cleaned_data.get('tamanio')
            perro_publicacion.sexo = form.cleaned_data.get('sexo')
            perro_publicacion.color = form.cleaned_data.get('color')
            perro_publicacion.edad = form.cleaned_data.get('edad')
            perro_publicacion.raza = form.cleaned_data.get('raza')
            perro_publicacion.save()

            publicacion.descripcion = form.cleaned_data.get('motivo_adopcion')
            publicacion.save()

            adopcion.origen = form.cleaned_data.get('origen')
            adopcion.motivo_adopcion = form.cleaned_data.get('motivo_adopcion')
            adopcion.save()

            messages.success(request, "¡Información actualizada correctamente!")
            return redirect(path_anterior)
    else:
        form = EditarAdopcionForm(initial={
            'nombre': perro_publicacion.nombre,
            'tamanio': perro_publicacion.tamanio,
            'sexo': perro_publicacion.sexo,
            'color': perro_publicacion.color,
            'edad': perro_publicacion.edad,
            'raza': perro_publicacion.raza,
            'motivo_adopcion': publicacion.descripcion,
            'origen': adopcion.origen,
        })
    context = {'form': form, 'errors': form.errors, 'path_anterior': path_anterior}
    return render(request, 'editar_adopcion.html', context)

def publicar_perro_perdido(request):
    if request.method == 'POST':
        form = PublicarPerroPerdidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            
            return redirect('/')
    else:
        form = PublicarPerroPerdidoForm()

    return render(request, 'publicar_perro_perdido.html', {'form': form})




def listar_perros_perdidos(request):
    perros_perdidos = Publicacion.objects.filter(id_perro_publicacion__activo=True, tipo_publicacion='Perdidos')
    return render(request, 'listar_perros.html', {'perros': paginar(request, perros_perdidos, 3)})





def cargar_perro_encontrado(request):
    if request.method == 'POST':
        form = CargarPerroEncontradoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            return redirect('/')
    else:
        form = CargarPerroEncontradoForm()

    return render(request, 'cargar_perro_encontrado.html', {'form': form})



def listar_perros_encontrados(request):
    perros_encontrados = Publicacion.objects.filter(id_perro_publicacion__activo=True, tipo_publicacion='Encontrado')
    return render(request, 'listar_perros.html', {'perros': paginar(request, perros_encontrados, 3)})




@login_required
def listar_mis_perros_encontrados(request):
    usuario = request.user  # Obtener el usuario autenticado
    publicaciones = Publicacion.objects.filter(id_usuario_id=usuario, tipo_publicacion='Encontrado')
    context = {
        'publicaciones': publicaciones
    }
    return render(request, 'listar_mis_perros.html', context)


@login_required
def listar_mis_perros_perdidos(request):
    usuario = request.user  # Obtener el usuario autenticado
    publicaciones = Publicacion.objects.filter(id_usuario_id=usuario, tipo_publicacion='Perdidos')
    context = {
        'publicaciones': publicaciones
    }
    return render(request, 'listar_mis_perros.html', context)



from .models import PostulacionPerdidosEncontrados

def contactarse_perro_perdido(request, id):
    publicacion = get_object_or_404(Publicacion, id_perro_publicacion_id=id, tipo_publicacion='Perdidos')

    esRegistrado = request.user.is_authenticated
    if esRegistrado:
        usuario = request.user
        if PostulacionPerdidosEncontrados.objects.filter(id_publicacion=id, email=usuario.email).exists():
            messages.error(request, 'Ya te has comunicado para esta publicación de perro perdido.')
            return redirect('listar_perro_perdidos', publicacion_id=id)
    else:
        email_postulante = request.POST.get('email')

        if publicacion.usuario.email == email_postulante:
            messages.error(request, 'No puedes contactarte con tu propia publicación.')
            return render(request, 'comunicarse_perro.html', {'success_message': 'Postulación enviada'})

        if PostulacionPerdidosEncontrados.objects.filter(id_publicacion=id, email=email_postulante).exists():
            messages.error(request, 'Ya te has comunicado para esta publicación de perro perdido.')
            return redirect('listar_perros_perdidos', publicacion_id=id)

    if request.method == 'POST':
        form = PostulacionForm(request.POST, esRegistrado=esRegistrado)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.id_publicacion = publicacion

            if esRegistrado:
                postulacion.nombre = usuario.nombre
                postulacion.apellido = usuario.apellido
                postulacion.email = usuario.email
                postulacion.telefono = usuario.telefono

            postulacion.save()

            subject = 'Postulación Exitosa'
            from_email = 'Ejtech <%s>' % settings.EMAIL_HOST_USER
            to_email = postulacion.email if esRegistrado else form.cleaned_data.get('email')
            reply_to_email = 'noreply@ejtechsoft.com'

            nombre_postulante = postulacion.nombre if esRegistrado else form.cleaned_data.get('nombre')

            context = {
                'nombre_postulante': nombre_postulante,
                'nombre_perro': postulacion.id_publicacion.nombre,
            }

            text_content = get_template('mail/postulacion_mail.txt')
            html_content = get_template('mail/postulacion_mail.html')
            text_content = text_content.render(context)
            html_content = html_content.render(context)

            email = EmailMultiAlternatives(subject, text_content, from_email, to=[to_email,], reply_to=[reply_to_email,])
            email.mixed_subtype = 'related'
            email.content_subtype = 'html'
            email.attach_alternative(html_content, 'text/html')
            email.send(fail_silently=False)

            enviar_postulante_a_publicador(postulacion, form.cleaned_data.get('mensaje'))
            messages.success(request, 'Postulación enviada')

            if esRegistrado:
                return redirect('listar_perros_perdidos', publicacion_id=id)
            else:
                return redirect('listar_perros_perdidos', publicacion_id=id)

    else:
        form = PostulacionForm()

    return render(request, 'postularse_perro_perdido.html', {'form': form, 'publicacion_id': id, 'esRegistrado': esRegistrado})
