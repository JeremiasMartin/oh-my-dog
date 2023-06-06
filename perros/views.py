from django.shortcuts import render, get_object_or_404, redirect
from .models import Perro, Atencion, Tipo_atencion 
from usuarios.models import Cliente
from .forms import perro_form, registrar_atencion_form, editar_foto_form
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from turnos.models import Turno
from django.db.models import Q
from turnos.views import paginar
from unidecode import unidecode


def listar_mascotas_cliente(request, cliente_id):
    mascotas = Perro.objects.filter(cliente_id__user_id=cliente_id)
    filtro = request.GET.get('filtro', None)
    
    if filtro:
        consulta_param = f"{filtro}-consulta"
        consulta = request.GET.get(consulta_param, None)

    if filtro and consulta:
        mascotas = buscar(request, filtro, consulta, mascotas)

    tamanio_opciones = (
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    )
    contexto = {
        "mascotas":paginar(request, mascotas, 6),
        "opciones_tamanios": tamanio_opciones
    }
    return render(request, 'listar_mascotas.html', contexto)

def registrar_mascota(request, cliente_id):
    cliente = get_object_or_404(Cliente, cliente_id=cliente_id)
    if request.method == 'POST':
        # Procesar el formulario de registro de mascota
        form = perro_form(request.POST, request.FILES)
        if form.is_valid():
            # Crear la mascota y guardarla en la base de datos
            nombre_mascota = form.cleaned_data['nombre']
            nombre_mascota_minuscula = nombre_mascota.lower()
            if Perro.objects.filter(cliente=cliente, nombre__iexact=nombre_mascota_minuscula).exists():
                messages.error(request, 'El cliente ya tiene una mascota con ese nombre registrada.')
            else: 
                mascota = form.save(commit=False)
                mascota.cliente = cliente
                mascota.save()
                messages.success(request, 'Mascota agregada exitosamente')
                return redirect('/usuarios/clientes')
    else:
        # Mostrar el formulario de registro de mascota
        form = perro_form()
    
    context={
        'form': form,
        'cliente':cliente,
    }
    return render(request, 'admin/registrar_mascota.html', context)

def editar_perfil_mascota(request, id):
    perro = get_object_or_404(Perro, id=id)
    cliente = get_object_or_404(Cliente, cliente_id=perro.cliente_id)
    if request.method == 'POST':
        form = perro_form(request.POST or None, request.FILES or None, instance=perro)
        if form.is_valid():
            nombre_mascota = form.cleaned_data['nombre']
            nombre_mascota_minuscula = nombre_mascota.lower()
            #chequea si el nombre existe, pero no incluye al mismo perro para asi poder cambiar a mayusculas y minusculas
            if Perro.objects.exclude(id=perro.id).filter(cliente=cliente, nombre__iexact=nombre_mascota_minuscula).exists():
                messages.error(request, 'El cliente ya tiene una mascota con ese nombre registrada.')
            else: 
                form.save()
                messages.success(request, '¡Información actualizada correctamente!')
                return redirect(f"/perros/listar-mascotas-cliente/{perro.cliente.user_id}/")
    else:
        form = perro_form(instance=perro)
    
    context = {
        'form': form, 
        'perro': perro
    }
    
    return render(request, 'editar_perfil_mascota.html', context)

def editar_foto_mi_mascota(request, id):
    perro = get_object_or_404(Perro, id=id)
    if request.method == 'POST':
        form = editar_foto_form(request.POST or None, request.FILES or None, instance=perro)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Información actualizada correctamente!')
            return redirect(f"/perros/listar-mascotas-cliente/{perro.cliente.user_id}/")
    else:
        form = editar_foto_form(instance=perro)

    context = {
        'form': form, 
        'mascota': perro
    }
    return render(request, 'editar_foto_mi_mascota.html', context)

def registrar_atencion(request, id_mascota):
    perro = get_object_or_404(Perro, id=id_mascota)
    tiene_error = False
    
    if request.method == 'POST':
        form = registrar_atencion_form(request.POST)
        if form.is_valid():
            atencion = form.save(commit=False)
            atencion.mascota = perro
            atencion.fecha = datetime.now()
            
            if atencion.tipo.tipo == 'Castración' and Atencion.objects.filter(mascota=perro, tipo__tipo='Castración').exists():
                messages.error(request, 'La mascota ya ha recibido una atención de tipo "Castración" anteriormente')
                tiene_error = True
            
            if atencion.tipo.tipo == 'Vacuna antirrábica' and Atencion.objects.filter(mascota=perro, tipo__tipo='Vacuna antirrábica').exists():
                # tiene mas de 4 meses porque recibió vacuna
                ultima_vacuna = Atencion.objects.filter(mascota=perro, tipo__tipo='Vacuna antirrábica').latest('fecha')
                ultima_vacuna_datetime = datetime.combine(ultima_vacuna.fecha, datetime.min.time())
                if (datetime.now() - ultima_vacuna_datetime) < timedelta(days=365):
                    messages.error(request, 'La mascota ya recibió una vacuna antirrábica hace menos de un año')
                    tiene_error = True

            if atencion.tipo.tipo == 'Vacuna antiviral' and Atencion.objects.filter(mascota=perro, tipo__tipo='Vacuna antiviral').exists():
                ultima_vacuna = Atencion.objects.filter(mascota=perro, tipo__tipo='Vacuna antiviral').latest('fecha')
                ultima_vacuna_datetime = datetime.combine(ultima_vacuna.fecha, datetime.min.time())
                if (date.today() - perro.fecha_nac).days < 120:
                    # tiene entre 2 y 4 meses
                    if(datetime.now() - ultima_vacuna_datetime) < timedelta(days=21):
                        # recibio la vacuna hace menos de 21
                        messages.error(request, 'La mascota ya recibió una vacuna antiviral hace menos de 21 días')
                        tiene_error = True
                else:
                    # tiene mas de 4 meses
                    if(datetime.now() - ultima_vacuna_datetime) < timedelta(days=365):
                        # recibio la vacuna hace menos de 1 año
                        messages.error(request, 'La mascota ya recibió una vacuna antiviral hace menos de un año')
                        tiene_error = True

            elif atencion.tipo.tipo == 'Vacuna antirrábica' and (date.today() - perro.fecha_nac).days > 120:
                turno = Turno.objects.create(
                    cliente_id=perro.cliente_id,
                    tipo_atencion_id=atencion.tipo.id,
                    fecha=date.today() + timedelta(days=365),
                    estado_id=3,
                )
            
            elif atencion.tipo.tipo == 'Vacuna antiviral' and (date.today() - perro.fecha_nac).days > 60:
                # tiene mas de 2 meses y no recibio vacuna en último periodo
                # Generación de turno 
                if (date.today()-perro.fecha_nac).days < 120:
                    # tiene menos de 4 meses
                    turno = Turno.objects.create(
                        cliente_id=perro.cliente_id,
                        tipo_atencion_id=atencion.tipo.id,
                        fecha=date.today() + timedelta(days=21),
                        estado_id=3,
                    )
                else:
                    turno = Turno.objects.create(
                        cliente_id=perro.cliente_id,
                        tipo_atencion_id=atencion.tipo.id,
                        fecha=date.today() + timedelta(days=365),
                        estado_id=3,
                    )
            else:
                if atencion.tipo.tipo == 'Vacuna antirrábica':
                    messages.error(request, 'Esta mascota es menor de 4 meses, no puede recibir la vacuna antirrábica')
                    tiene_error = True
                elif(atencion.tipo.tipo == 'Vacuna antiviral'):
                        messages.error(request, 'Esta mascota es menor de 2 meses, no puede recibir la vacuna antiviral')
                        tiene_error = True
            
            if not tiene_error:
                atencion.save()
                messages.success(request, 'Atención registrada exitosamente')
                return redirect(f'/perros/registrar-atencion/{perro.id}/')
    else:
        form = registrar_atencion_form()
    context={
        'form': form,
        'perro': perro,
    }
    return render(request, 'admin/registrar_atencion.html', context)

def ver_historia_clinica(request, id_mascota):
    perro = get_object_or_404(Perro, id=id_mascota)
    atenciones = Atencion.objects.filter(mascota_id=id_mascota)
    # Para filtrar las atenciones
    tipos = Tipo_atencion.objects.all()
    tipos_dict = {}
    for tipo in tipos:
        tipos_dict[tipo.tipo] = tipo.id
    vacunas = atenciones.filter(Q(tipo_id=tipos_dict['Vacuna antiviral']) | Q(tipo_id=tipos_dict['Vacuna antirrábica']))
    clinicas = atenciones.exclude(Q(tipo_id=tipos_dict['Vacuna antiviral']) | Q(tipo_id=tipos_dict['Vacuna antirrábica']))
    context = {
        "perro": perro,
        "clinicas": clinicas,
        'vacunas': vacunas
    }
    return render(request, 'ver_historia_clinica.html', context)

def listar_vacunas(request, id_mascota):
    perro = get_object_or_404(Perro, id=id_mascota)
    atenciones = Atencion.objects.filter(mascota_id=id_mascota)
    # Para filtrar las atenciones
    tipos = Tipo_atencion.objects.all()
    tipos_dict = {}
    for tipo in tipos:
        tipos_dict[tipo.tipo] = tipo.id
    vacunas = atenciones.filter(Q(tipo_id=tipos_dict['Vacuna antiviral']) | Q(tipo_id=tipos_dict['Vacuna antirrábica']))
    context = {
        "perro": perro,
        'vacunas': vacunas
    }
    return render(request, 'listar_vacunas.html', context)

def buscar(request, filtro, consulta, mascotas):
    print("FILTRO",filtro)
    print("CONSULTA",consulta)
    
    if filtro == 'tamanio':
        mascotas_filtradas = mascotas.filter(tamanio=consulta)
        
    elif filtro == 'raza':
        mascotas_filtradas = mascotas.filter(raza__icontains=unidecode(consulta))
    
    if  not mascotas_filtradas:
        messages.add_message(request, messages.ERROR, 'No hay perros para la búsqueda realizada')
        mascotas_filtradas = mascotas

    return mascotas_filtradas