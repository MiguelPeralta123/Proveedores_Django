from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from threading import Timer
from datetime import datetime, time
import csv
import os
from .forms import *
from .models import *
from .options import *
from iniciar_sesion.models import CustomUser

# Creating a unique id for each request
import random
import string


def generar_codigo_unico():
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(10))
    return codigo

# VISTA DE INICIO
# Decorator to force login. The return route is defined in proveedores/settings.py
@login_required
def home(request):
    return render(request, 'home.html', {
        'current_user': request.user,
    })


# VISTAS DE MATERIAL (GET ALL, CREATE, DETAIL)

@login_required
def material(request):
    try:
        if request.user.puede_crear_material or request.user.compras or request.user.finanzas or request.user.sistemas:
            
            # Si el usuario es administrador, podrá ver una lista con TODAS las solicitudes
            #if request.user.is_superuser:
            #    all_solicitudes = MaterialSolicitud.objects.all().order_by('id')
            
            # Inicializar la lista de mis_solicitudes
            mis_solicitudes = []

            if request.user.compras:
                solicitudes = MaterialSolicitud.objects.filter(pendiente=True).order_by('id')
                if request.user.puede_crear_material:
                    mis_solicitudes = MaterialSolicitud.objects.filter(usuario=request.user).order_by('id')
            elif request.user.finanzas:
                solicitudes = MaterialSolicitud.objects.filter(compras=True).order_by('id')
                if request.user.puede_crear_material:
                    mis_solicitudes = MaterialSolicitud.objects.filter(usuario=request.user).order_by('id')
            elif request.user.sistemas:
                solicitudes = MaterialSolicitud.objects.filter(finanzas=True).order_by('id')
                if request.user.puede_crear_material:
                    mis_solicitudes = MaterialSolicitud.objects.filter(usuario=request.user).order_by('id')
            else:
                solicitudes = MaterialSolicitud.objects.filter(usuario=request.user).order_by('id')
                solicitudes_borradores = solicitudes.filter(borrador=True).order_by('id')
                solicitudes_pendientes = solicitudes.filter(
                    Q(pendiente=True) | 
                    Q(compras=True) | 
                    Q(finanzas=True)
                ).order_by('id')
                solicitudes_rechazadas = solicitudes.filter(
                    Q(rechazado_compras=True) | 
                    Q(rechazado_finanzas=True) | 
                    Q(rechazado_sistemas=True)
                ).order_by('id')
                solicitudes_aprobadas = solicitudes.filter(sistemas=True).order_by('id')
                solicitudes_eliminadas = solicitudes.filter(eliminado=True).order_by('id')

                historial = []
                for solicitud in solicitudes:
                    historial += MaterialHistorial.objects.filter(id_solicitud=solicitud.id).order_by('id')
                
                return render(request, 'material/material.html', {
                    'solicitudes': solicitudes,
                    'historial': historial,
                    'solicitudes_borradores': solicitudes_borradores,
                    'solicitudes_pendientes': solicitudes_pendientes,
                    'solicitudes_rechazadas': solicitudes_rechazadas,
                    'solicitudes_aprobadas': solicitudes_aprobadas,
                    'solicitudes_eliminadas': solicitudes_eliminadas,
                    'current_user': request.user
                })

            # Si el usuario es autorizador y puede crear solicitudes, incluir las listas para los filtros
            if request.user.puede_crear_material:
                solicitudes_borradores = mis_solicitudes.filter(borrador=True).order_by('id')
                solicitudes_pendientes = mis_solicitudes.filter(
                    Q(pendiente=True) | 
                    Q(compras=True) | 
                    Q(finanzas=True)
                ).order_by('id')
                solicitudes_rechazadas = mis_solicitudes.filter(
                    Q(rechazado_compras=True) | 
                    Q(rechazado_finanzas=True) | 
                    Q(rechazado_sistemas=True)
                ).order_by('id')
                solicitudes_aprobadas = mis_solicitudes.filter(sistemas=True).order_by('id')
                solicitudes_eliminadas = mis_solicitudes.filter(eliminado=True).order_by('id')

            historial = []
            #if request.user.is_superuser:  
            #    historial = MaterialHistorial.objects.all()
            #else:
            for solicitud in solicitudes:
                if solicitud not in mis_solicitudes:
                    historial += MaterialHistorial.objects.filter(id_solicitud=solicitud.id).order_by('id')
            for solicitud in mis_solicitudes:
                historial += MaterialHistorial.objects.filter(id_solicitud=solicitud.id).order_by('id')

            if request.user.puede_crear_material:
                if request.user.is_superuser:
                    return render(request, 'material/material.html', {
                        'solicitudes': solicitudes,
                        'mis_solicitudes': mis_solicitudes,
                        'solicitudes_borradores': solicitudes_borradores,
                        'solicitudes_pendientes': solicitudes_pendientes,
                        'solicitudes_rechazadas': solicitudes_rechazadas,
                        'solicitudes_aprobadas': solicitudes_aprobadas,
                        'solicitudes_eliminadas': solicitudes_eliminadas,
                        #'all_solicitudes': all_solicitudes,
                        'historial': historial,
                        'current_user': request.user
                    })
                else:
                    return render(request, 'material/material.html', {
                        'solicitudes': solicitudes,
                        'mis_solicitudes': mis_solicitudes,
                        'solicitudes_borradores': solicitudes_borradores,
                        'solicitudes_pendientes': solicitudes_pendientes,
                        'solicitudes_rechazadas': solicitudes_rechazadas,
                        'solicitudes_aprobadas': solicitudes_aprobadas,
                        'solicitudes_eliminadas': solicitudes_eliminadas,
                        'historial': historial,
                        'current_user': request.user
                    })
            else:
                if request.user.is_superuser:
                    return render(request, 'material/material.html', {
                        'solicitudes': solicitudes,
                        #'all_solicitudes': all_solicitudes,
                        'historial': historial,
                        'current_user': request.user
                    })
                else:
                    return render(request, 'material/material.html', {
                        'solicitudes': solicitudes,
                        'historial': historial,
                        'current_user': request.user
                    })
        else:
            return redirect('home')
    
    except Exception as e:
        print(f"Se produjo un error al cargar los materiales: {str(e)}")
        return redirect('home')


# Si el usuario es administrador, podrá ver una lista con TODAS las solicitudes
def get_all_material_requests(request):
    if request.user.is_superuser:
        historial = MaterialHistorial.objects.all()
        all_solicitudes = MaterialSolicitud.objects.all().order_by('id').reverse()
        data = [
            {
                'id': solicitud.id,
                'id_solicitud': solicitud.id_solicitud,
                'es_migracion': solicitud.es_migracion,
                'empresa_origen': solicitud.empresa_origen,
                'empresa_destino': solicitud.empresa_destino,
                'nombre_producto_migracion': solicitud.nombre_producto_migracion,
                'empresa': solicitud.empresa,
                'justificacion': solicitud.justificacion,
                'fecha': solicitud.fecha,
                'usuario': solicitud.usuario.get_full_name() if solicitud.usuario else None,
                'comentarios': solicitud.comentarios,
                'pendiente': solicitud.pendiente,
                'compras': solicitud.compras,
                'finanzas': solicitud.finanzas,
                'sistemas': solicitud.sistemas,
                'aprobadas': solicitud.aprobadas,
                'rechazado_compras': solicitud.rechazado_compras,
                'rechazado_finanzas': solicitud.rechazado_finanzas,
                'rechazado_sistemas': solicitud.rechazado_sistemas,
                'eliminado': solicitud.eliminado,
                'borrador': solicitud.borrador,
            } for solicitud in all_solicitudes
        ]
        historialData = [
            {
                'id_solicitud': registro.id_solicitud,
                'message': "Solicitud " + registro.accion + " por " + registro.usuario.get_full_name(),
                'fecha': registro.fecha,
            } for registro in historial
        ]
        return JsonResponse({'all_solicitudes': data, 'historial': historialData})



@login_required
def create_material_form(request):
    try:
        material_id = request.GET.get('material_id')
        if material_id:
            material_instance = get_object_or_404(Material, pk=material_id)
            material_form = MaterialForm(instance=material_instance)
        else:
            material_form = MaterialForm()
        # Renderiza el formulario como HTML
        material_form_html = material_form.as_p()
        # Devuelve el HTML del formulario en la respuesta JSON
        return JsonResponse({'material_form': material_form_html})
    
    except Exception as e:
        print(f"Se produjo un error al crear el formulario de material: {str(e)}")
        return redirect('home')


@login_required
@require_POST
def save_material_form(request):
    if request.method == 'POST':
        # Obtén los datos del formulario del cuerpo de la solicitud
        id_solicitud = request.POST.get('id_solicitud')
        tipo_alta = request.POST.get('tipo_alta')
        subfamilia = request.POST.get('subfamilia')
        nombre_producto = request.POST.get('nombre_producto')
        largo = request.POST.get('largo')
        ancho = request.POST.get('ancho')
        alto = request.POST.get('alto')
        um_largo = request.POST.get('um_largo')
        um_ancho = request.POST.get('um_ancho')
        um_alto = request.POST.get('um_alto')
        material = request.POST.get('material')
        color = request.POST.get('color')
        marca = request.POST.get('marca')
        parte_modelo = request.POST.get('parte_modelo')
        nombre_comun = request.POST.get('nombre_comun')
        es_mezcla = True if request.POST.get('es_mezcla') == 'on' else False
        ing_activo = request.POST.get('ing_activo')
        porcentaje_iva = request.POST.get('porcentaje_iva')
        alias = request.POST.get('alias')
        unidad_medida = request.POST.get('unidad_medida')
        codigo_sat = request.POST.get('codigo_sat')
        es_material_empaque = True if request.POST.get('es_material_empaque') == 'on' else False
        es_prod_terminado = True if request.POST.get('es_prod_terminado') == 'on' else False
        
        # Obtener la imagen y ficha técnica del formulario
        foto_producto = request.FILES.get('foto_producto')
        ficha_tecnica = request.FILES.get('ficha_tecnica')

        # Crea y guarda una instancia de Material
        material_servicio = Material(id_solicitud=id_solicitud, tipo_alta=tipo_alta, subfamilia=subfamilia, nombre_producto=nombre_producto, largo=largo, ancho=ancho, alto=alto, um_largo=um_largo, um_ancho=um_ancho, um_alto=um_alto, material=material, color=color, marca=marca, parte_modelo=parte_modelo, nombre_comun=nombre_comun, es_mezcla=es_mezcla, ing_activo=ing_activo, porcentaje_iva=porcentaje_iva, alias=alias, unidad_medida=unidad_medida, codigo_sat=codigo_sat, es_material_empaque=es_material_empaque, es_prod_terminado=es_prod_terminado)

        # Añadir los archivos a la instancia de material
        material_servicio.foto_producto = foto_producto
        material_servicio.ficha_tecnica = ficha_tecnica

        material_servicio.save()

        # Devuelve una respuesta exitosa
        return JsonResponse({'message': 'Material guardado exitosamente.'})
    else:
        # Si la solicitud no es de tipo POST, devuelves un error
        return JsonResponse({'error': 'Se esperaba una solicitud POST.'}, status=400)


@login_required
def get_request_materials(request):
    try:
        id_solicitud = request.GET.get('id_solicitud')
        materiales = Material.objects.filter(id_solicitud=id_solicitud).order_by('id')
        data = [
            {
                'tipo_alta': material.tipo_alta,
                'subfamilia': material.subfamilia,
                'nombre_producto': material.nombre_producto,
                'foto_producto': ('<img style="width: auto; max-height: 4rem" src="' + material.foto_producto.url + '" alt="Foto del producto"/>') if material.foto_producto else 'Sin foto',
                'ficha_tecnica': ('<img style="width: auto; max-height: 4rem" src="' + material.ficha_tecnica.url + '" alt="Ficha técnica"/>') if  material.ficha_tecnica else 'Sin ficha técnica',
                'largo': (material.largo + ' ' + material.um_largo) if material.um_largo else material.largo,
                'ancho': (material.ancho + ' ' + material.um_ancho) if material.um_ancho else material.ancho,
                'alto': (material.alto + ' ' + material.um_alto) if material.um_alto else material.alto,
                'material': material.material,
                'color': material.color,
                'marca': material.marca,
                'parte_modelo': material.parte_modelo,
                'nombre_comun': material.nombre_comun,
                'ing_activo': material.ing_activo,
                'porcentaje_iva': material.porcentaje_iva,
                'alias': material.alias,
                'unidad_medida': material.unidad_medida,
                'codigo_sat': material.codigo_sat,
                'es_mezcla': 'Si' if material.es_mezcla else 'No',
                'es_material_empaque': 'Si' if material.es_material_empaque else 'No',
                'es_prod_terminado': 'Si' if material.es_prod_terminado else 'No',
                'acciones': 
                    '<div class="d-flex gap-2"><button id="edit_material_' 
                    + str(material.id) 
                    + '" class="btn btn-warning edit_material" type="button" style="font-size:0.8rem" data-bs-toggle="modal" data-bs-target="#modalId"><i class="fa fa-pencil" id="icon-material-' 
                    + str(material.id) 
                    + '" aria-hidden="true"></i></button>' 
                    + '<button id="remove_material_' 
                    + str(material.id) 
                    + '" class="btn btn-danger remove_material" onclick="confirmAndDelete(' 
                    + str(material.id) 
                    + ')" type="button" style="font-size:0.8rem"><i class="fa fa-trash" aria-hidden="true"></i></button></div>',
            } for material in materiales
        ]
        return JsonResponse({'materiales': data})
    
    except Exception as e:
        print(f"Se produjo un error al cargar los materiales: {str(e)}")
        return redirect('home')


@login_required
def delete_material(request, id):
    try:
        if request.method == 'POST':
            material = get_object_or_404(Material, pk=id)
            if material:
                material.delete()
                return JsonResponse({'message': 'Material eliminado con éxito'})
            else:
                return JsonResponse({'error': 'Material no encontrado'})
        else:
            return JsonResponse({'error': 'Método no permitido'})
        
    except Exception as e:
        return JsonResponse({'error': f"Se produjo un error al eliminar el material: {str(e)}"})


@login_required
def material_create(request):
    try:
        if request.user.puede_crear_material:
            #MaterialFormSet = formset_factory(MaterialForm, extra=0)

            if request.method == 'GET':
                default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}

                solicitud_form = SolicitudForm(initial=default_values)
                material_form = MaterialForm()
                id_solicitud = generar_codigo_unico()
                #material_formset = MaterialFormSet(prefix='material', initial=[{}])

                # Cargando los registros de materiales desde el archivo catalogo_productos.csv
                csv_path = os.path.join('csv_files', 'catalogo_productos.csv')
                with open(csv_path, 'r') as csv_file:
                    # Lee el archivo CSV
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader) # Skipping headers
                    
                    # Inicializa la lista que contendrá las tuplas
                    catalogo_material = []
                    
                    # Itera sobre cada fila del archivo CSV
                    for row in csv_reader:
                        # Extrae la información necesaria de las columnas
                        codigo = row[0]
                        nombre_producto = row[1]
                        
                        # Crea la cadena de texto con el formato deseado
                        formato = f'{codigo} - {nombre_producto}'
                        
                        # Agrega la tupla a la lista
                        catalogo_material.append({'value': nombre_producto, 'text': formato})

                return render(request, 'material/material_create.html', {
                    'solicitud_form': solicitud_form,
                    #'material_formset': material_formset,
                    'material_form': material_form,
                    'id_solicitud': id_solicitud,
                    'catalogo_material': catalogo_material,
                    'subfamilia_producto_list': SUBFAMILIA_PRODUCTO_LIST,
                    'subfamilia_servicio_list': SUBFAMILIA_SERVICIO_LIST,
                    'unidad_medida_list': UNIDAD_MEDIDA_LIST,
                    'current_user': request.user,
                })
            else:
                try:
                    solicitud_form = SolicitudForm(request.POST)
                    #material_formset = MaterialFormSet(request.POST, request.FILES, prefix='material')
                    historial_form = HistorialForm(request.POST)

                    if solicitud_form.is_valid() and historial_form.is_valid():
                        #id_solicitud = generar_codigo_unico()
                        solicitud = solicitud_form.save(commit=False)
                        #solicitud.id_solicitud = id_solicitud
                        solicitud.usuario = request.user
                        solicitud.save()

                        if not solicitud.es_migracion:
                            if material_formset.is_valid():
                                for material_form in material_formset:
                                    if not material_form.cleaned_data.get('tipo_alta') or not material_form.cleaned_data.get('subfamilia') or not material_form.cleaned_data.get('nombre_producto') or not material_form.cleaned_data.get('porcentaje_iva') or not material_form.cleaned_data.get('unidad_medida'):
                                        continue  # Saltar formularios con campos requeridos vacíos
                                    material = material_form.save(commit=False)
                                    material.id_solicitud = id_solicitud
                                    material.save()
                            else:
                                for form in material_formset:
                                    if form.errors:
                                        print(form.errors)
                        
                        # Guardar la creacion de la solicitud en el historial de cambios
                        historial = historial_form.save(commit=False)
                        historial.id_solicitud = solicitud.id
                        historial.accion = 'creada'
                        historial.usuario = request.user
                        historial.save()

                        # Enviar correo electrónico
                        if not solicitud.borrador:
                            subject = 'Nueva solicitud de material'
                            message = str(request.user.get_full_name()) + ' ha solicitado un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/'
                            from_email = 'altaproveedoresricofarms@gmail.com'
                            recipient_list = []
                            if solicitud.es_migracion:
                                autorizadores = CustomUser.objects.filter(sistemas = True)
                            else:
                                autorizadores = CustomUser.objects.filter(compras = True)
                            for autorizador in autorizadores:
                                recipient_list.append(autorizador.email)
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                        return redirect('material')
                    
                except ValueError as e:
                    default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}
                    
                    solicitud_form = SolicitudForm(initial=default_values)
                    material_formset = MaterialFormSet(prefix='material', initial=[{}])

                    return render(request, 'material/material_create.html', {
                        'solicitud_form': solicitud_form,
                        'material_formset': material_formset,
                        'error': str(e),
                        'current_user': request.user,
                    })
        else:
            return redirect('material')
    
    except Exception as e:
        print(f"Se produjo un error al crear el material: {str(e)}")
        return redirect('home')


@login_required
def material_detail(request, material_id):
    try:
        solicitud = get_object_or_404(MaterialSolicitud, pk=material_id)
        materiales = Material.objects.filter(id_solicitud=solicitud.id_solicitud)
        
        MaterialFormSet = formset_factory(MaterialForm, extra=0)

        if request.method == 'GET':
            default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                            'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}
            
            if request.user.compras and solicitud.compras:
                solicitud_form = SolicitudFormForCompras(
                    instance=solicitud, initial=default_values)
            elif request.user.finanzas and solicitud.finanzas:
                solicitud_form = SolicitudFormForFinanzas(
                    instance=solicitud, initial=default_values)
            elif request.user.sistemas and solicitud.sistemas:
                solicitud_form = SolicitudFormForSistemas(
                    instance=solicitud, initial=default_values)
            else:
                solicitud_form = SolicitudDetailForm(
                    instance=solicitud, initial=default_values)
                
            material_formset = MaterialFormSet(prefix='material', initial=[{}])

            material_forms = [MaterialDetailForm(
                instance=material, prefix=f'material-{material.id}') for material in materiales]
            
            # Cargando los registros de materiales desde el archivo catalogo_productos.csv
            csv_path = os.path.join('csv_files', 'catalogo_productos.csv')
            with open(csv_path, 'r') as csv_file:
                # Lee el archivo CSV
                csv_reader = csv.reader(csv_file)
                next(csv_reader) # Skipping headers
                
                # Inicializa la lista que contendrá las tuplas
                catalogo_material = []
                
                # Itera sobre cada fila del archivo CSV
                for row in csv_reader:
                    # Extrae la información necesaria de las columnas
                    codigo = row[0]
                    nombre_producto = row[1]
                    
                    # Crea la cadena de texto con el formato deseado
                    formato = f'{codigo} - {nombre_producto}'
                    
                    # Agrega la tupla a la lista
                    catalogo_material.append({'value': nombre_producto, 'text': formato})

            # Si la solicitud está rechazada o es un borrador, el solicitante podrá añadir nuevos elementos
            return render(request, 'material/material_detail.html', {
                'solicitud': solicitud,
                'solicitud_form': solicitud_form,
                'materiales': materiales,
                'material_forms': material_forms,
                'material_formset': material_formset,
                'catalogo_material': catalogo_material,
                'subfamilia_producto_list': SUBFAMILIA_PRODUCTO_LIST,
                'subfamilia_servicio_list': SUBFAMILIA_SERVICIO_LIST,
                'unidad_medida_list': UNIDAD_MEDIDA_LIST,
                'current_user': request.user,
            })
        else:
            try:
                if request.user.compras and solicitud.compras:
                    solicitud_form = SolicitudFormForCompras(
                        request.POST, instance=solicitud)
                elif request.user.finanzas and solicitud.finanzas:
                    solicitud_form = SolicitudFormForFinanzas(
                        request.POST, instance=solicitud)
                elif request.user.sistemas and solicitud.sistemas:
                    solicitud_form = SolicitudFormForSistemas(
                        request.POST, instance=solicitud)
                else:
                    solicitud_form = SolicitudDetailForm(
                        request.POST, instance=solicitud)
                    # Solo el solicitante podrá añadir más elementos a la solicitud
                    material_formset = MaterialFormSet(request.POST, request.FILES, prefix='material')

                material_forms = [MaterialDetailForm(
                    request.POST, request.FILES, instance=material, prefix=f'material-{material.id}') for material in materiales]
                
                historial_form = HistorialForm(request.POST)

                notificarContabilidad = False

                if solicitud_form.is_valid() and historial_form.is_valid():
                    solicitud_form.save()

                    if not solicitud.es_migracion:
                        # Guardando los materiales que ya estaban
                        if all(form.is_valid() for form in material_forms):
                            materialesAprobados = ''
                            serviciosAprobados = ''
                            for form in material_forms:
                                # Saltar formularios con campos requeridos vacíos
                                if not form.cleaned_data.get('tipo_alta') or not form.cleaned_data.get('subfamilia') or not form.cleaned_data.get('nombre_producto') or not form.cleaned_data.get('porcentaje_iva') or not form.cleaned_data.get('unidad_medida'):
                                    continue
                                if form.cleaned_data.get('tipo_alta') == 'Almacén':
                                    materialesAprobados += '\n' + form.cleaned_data.get('codigo') + ' - ' + form.cleaned_data.get('nombre_producto')
                                if form.cleaned_data.get('tipo_alta') == 'Servicio':
                                    serviciosAprobados += '\n' + form.cleaned_data.get('codigo') + ' - ' + form.cleaned_data.get('nombre_producto')
                                    # Si la solicitud aprobada incluye un servicio, se debe notificar a contabilidad
                                    notificarContabilidad = True
                                form.save()

                        # Guardando los materiales que se hayan añadido a la solicitud
                        if material_formset.is_valid():
                            for material_form in material_formset:
                                # Saltar formularios con campos requeridos vacíos
                                if not material_form.cleaned_data.get('tipo_alta') or not material_form.cleaned_data.get('subfamilia') or not material_form.cleaned_data.get('nombre_producto') or not material_form.cleaned_data.get('porcentaje_iva') or not material_form.cleaned_data.get('unidad_medida'):
                                    continue
                                if material_form.cleaned_data.get('tipo_alta') == 'Servicio':
                                    # Si la solicitud aprobada incluye un servicio, se debe notificar a contabilidad
                                    notificarContabilidad = True
                                material = material_form.save(commit=False)
                                material.id_solicitud = solicitud.id_solicitud
                                print('Guardando ' + form.cleaned_data.get('nombre_producto'))
                                material.save()
                        else:
                            for form in material_formset:
                                if form.errors:
                                    print(form.errors)
                    
                    # Guardar la modificación de la solicitud en el historial de cambios
                    historial = historial_form.save(commit=False)
                    historial.id_solicitud = solicitud.id
                    if solicitud.rechazado_compras or solicitud.rechazado_finanzas or solicitud.rechazado_sistemas:
                        historial.accion = 'rechazada'
                        action = 'rechazado'
                    elif solicitud.pendiente or solicitud.compras or solicitud.finanzas:
                        historial.accion = 'modificada'
                        action = 'modificado'
                    elif solicitud.eliminado:
                        historial.accion = 'eliminada'
                        action = 'eliminado'
                    elif solicitud.sistemas:
                        historial.accion = 'registrada'
                        action = 'registrado'
                    historial.usuario = request.user
                    historial.save()

                    # Recorremos los materiales para filtrar los rechazados
                    material_rechazado_forms = []
                    id_solicitud = generar_codigo_unico()
                    for material in materiales:
                        # Verifica si el material está marcado como rechazado
                        if material.rechazado:
                            # Al crear una nueva solicitud, ningún material estará rechazado
                            material.rechazado = False
                            material.id_solicitud = id_solicitud
                            material.save()
                            material_form = MaterialDetailForm(
                                request.POST, instance=material, prefix=f'material-{material.id}'
                            )
                            material_rechazado_forms.append(material_form)
                    
                    # Los productos rechazados se agruparán en una nueva solicitud
                    if len(material_rechazado_forms) > 0:
                        solicitud_new_form = SolicitudForm(request.POST)
                        material_formset = material_rechazado_forms
                        historial_form = HistorialForm(request.POST)
                        historial_form_2 = HistorialForm(request.POST)

                        if solicitud_new_form.is_valid() and historial_form.is_valid():
                            new_solicitud = solicitud_new_form.save(commit=False)
                            new_solicitud.id_solicitud = id_solicitud
                            new_solicitud.usuario = solicitud.usuario

                            # Copiar el comentario en la nueva solicitud
                            new_solicitud.comentarios = solicitud.comentarios

                            # Eliminar el comentario de la solicitud aprobada
                            solicitud.comentarios = ''
                            solicitud_form.save()

                            # Cambiar el estatus de la nueva solicitud a rechazado
                            if new_solicitud.finanzas == True:
                                new_solicitud.finanzas = False
                                new_solicitud.rechazado_compras = True
                            if new_solicitud.aprobadas == True:
                                new_solicitud.aprobadas = False
                                new_solicitud.rechazado_sistemas = True
                            new_solicitud.save()

                            if new_solicitud.es_migracion == False:
                                for material_form in material_formset:
                                    material = material_form.save(commit=False)
                                    material.id_solicitud = id_solicitud
                                    material.save()
                            
                            # Guardar la creación de la solicitud en el historial de cambios
                            historial = historial_form.save(commit=False)
                            historial.id_solicitud = new_solicitud.id
                            historial.accion = 'creada'
                            historial.usuario = new_solicitud.usuario
                            historial.save()
                            
                            # Guardar la modificación de la solicitud en el historial de cambios
                            historial2 = historial_form_2.save(commit=False)
                            historial2.id_solicitud = new_solicitud.id
                            historial2.accion = 'rechazada'
                            historial2.usuario = request.user
                            historial2.save()

                            # Enviar correo electrónico para materiales rechazados
                            subject = 'Solicitud de material modificada'
                            message = str(request.user.get_full_name()) + ' ha rechazado un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/\nComentario: ' + solicitud.comentarios
                            from_email = 'altaproveedoresricofarms@gmail.com'
                            recipient_list = [solicitud.usuario.email]
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                    # Enviar correo electrónico
                    # Asunto
                    if action == 'rechazado':
                        subject = 'Solicitud de material rechazada'
                    elif action == 'registrado':
                        subject = 'Solicitud de material registrada'
                    else:
                        subject = 'Solicitud de material modificada'

                    # Mensaje
                    if action == 'rechazado':
                        message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/\nComentario: ' + solicitud.comentarios
                    if action == 'registrado':
                        message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/\n\nMateriales aprobados:' + materialesAprobados + '\n\nServicios aprobados:' + serviciosAprobados
                    else:
                        message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/'

                    # Remitente
                    from_email = 'altaproveedoresricofarms@gmail.com'

                    # Destinatario
                    recipient_list = [solicitud.usuario.email]
                    # Si se registra un servicio en Agrosmart, se notifica a contabilidad
                    if action == 'registrado' and notificarContabilidad:
                        recipient_list.append('contadorsr@ricofarms.com')
                    elif action != 'rechazado':
                        if request.user.compras or request.user.finanzas:
                            autorizadores = CustomUser.objects.filter(sistemas=True)
                        else:
                            recipient_list = []
                            autorizadores = CustomUser.objects.filter(compras=True)
                        for autorizador in autorizadores:
                            recipient_list.append(autorizador.email)

                    # Enviar correo
                    #if not solicitud.eliminado:
                        #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                    return redirect('material')

            except ValueError:
                solicitud_form = SolicitudForm(instance=material)
                return render(request, 'material/material_detail.html', {
                    'solicitud': solicitud,
                    'form': solicitud_form,
                    'error': 'Se produjo un error al actualizar, intente de nuevo',
                    'current_user': request.user,
                })
    
    except Exception as e:
        print(f"Se produjo un error al cargar el material: {str(e)}")
        return redirect('home')


# ENVIANDO UN CORREO DE RECORDATORIO CADA 30 MINUTOS

def enviarCorreo(departamento, elementos, folios):
    cadenaFolios = ''
    for folio in folios:
        cadenaFolios += '\n' + folio

    subject = 'Recordatorio de solicitudes por aprobar'
    message = 'Tiene ' + str(elementos) + ' solicitudes de alta de material pendientes de aprobación. Por favor ingrese a http://23.19.74.40:8001/materiales/ para revisarlas.' + cadenaFolios

    from_email = 'altaproveedoresricofarms@gmail.com'
    
    recipient_list = []
    if departamento == 'compras':
        autorizadores = CustomUser.objects.filter(compras = True)
    if departamento == 'finanzas':
        autorizadores = CustomUser.objects.filter(finanzas = True)
    if departamento == 'sistemas':
        autorizadores = CustomUser.objects.filter(sistemas = True)

    for autorizador in autorizadores:
        recipient_list.append(autorizador.email)

    #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

def solicitudesPendientes():
    current_day = datetime.now().weekday()
    current_time = datetime.now().time()
    start_time = time(7, 0)
    end_time = time(19, 0)
    end_time_saturday = time(15, 0)

    # Los correos de recordatorio solo se envían de lunes a viernes entre 7am y 7pm y los sabados entre 7am y 3pm
    if 0 <= current_day <= 4 and start_time <= current_time <= end_time or current_day == 5 and start_time <= current_time <= end_time_saturday:

        # Revisar si hay solicitudes de material pendientes de aprobar por compras
        solicitudes_compras = MaterialSolicitud.objects.filter(pendiente=True)
        if len(solicitudes_compras) > 0:
            folios = []
            for solicitud in solicitudes_compras:
                if solicitud.justificacion != '':
                    folios.append(str(solicitud.id) + ' - ' + solicitud.justificacion)
                else:
                    folios.append(str(solicitud.id) + ' - ' + solicitud.nombre_producto_migracion)
            enviarCorreo('compras', len(solicitudes_compras), folios)

        # Revisar si hay solicitudes de material pendientes de aprobar por finanzas
        solicitudes_finanzas = MaterialSolicitud.objects.filter(compras=True)
        if len(solicitudes_finanzas) > 0:
            folios = []
            for solicitud in solicitudes_finanzas:
                if solicitud.justificacion != '':
                    folios.append(str(solicitud.id) + ' - ' + solicitud.justificacion)
                else:
                    folios.append(str(solicitud.id) + ' - ' + solicitud.nombre_producto_migracion)
            enviarCorreo('finanzas', len(solicitudes_finanzas), folios)

        # Revisar si hay solicitudes de cliente / solicitud pendientes de aprobar por sistemas
        solicitudes_sistemas = MaterialSolicitud.objects.filter(finanzas=True)
        if len(solicitudes_sistemas) > 0:
            folios = []
            for solicitud in solicitudes_sistemas:
                if solicitud.justificacion != '':
                    folios.append(str(solicitud.id) + ' - ' + solicitud.justificacion)
                else:
                    folios.append(str(solicitud.id) + ' - ' + solicitud.nombre_producto_migracion)
            enviarCorreo('sistemas', len(solicitudes_sistemas), folios)

    # El correo de recordatorio debe enviarse cada 2 horas
    Timer(7200, solicitudesPendientes).start()

#solicitudesPendientes()