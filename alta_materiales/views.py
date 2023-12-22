from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.core.mail import send_mail
from django.db.models import Q
import json
from django.http import JsonResponse
from threading import Timer
from datetime import datetime, time
import csv
import os
from .forms import *
from .models import *
from .options import *

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
    return render(request, 'home.html')


# VISTAS DE MATERIAL (GET ALL, CREATE, DETAIL)

@login_required
def material(request):
    try:
        if request.user.puede_crear_material or request.user.compras or request.user.finanzas or request.user.sistemas:
            
            # Si el usuario es administrador, podrá ver una lista con TODAS las solicitudes
            if request.user.is_superuser:
                all_solicitudes = MaterialSolicitud.objects.all().order_by('id')
            
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
            if request.user.is_superuser:  
                historial = MaterialHistorial.objects.all()
            else:
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
                        'all_solicitudes': all_solicitudes,
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
                        'all_solicitudes': all_solicitudes,
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
        


@login_required
def material_create(request):
    try:
        if request.user.puede_crear_material:
            MaterialFormSet = formset_factory(MaterialForm, extra=0)

            if request.method == 'GET':
                default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}

                solicitud_form = SolicitudForm(initial=default_values)
                material_formset = MaterialFormSet(prefix='material', initial=[{}])

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
                    'material_formset': material_formset,
                    'catalogo_material': catalogo_material,
                    'subfamilia_producto_list': SUBFAMILIA_PRODUCTO_LIST,
                    'subfamilia_servicio_list': SUBFAMILIA_SERVICIO_LIST,
                    'unidad_medida_list': UNIDAD_MEDIDA_LIST,
                })
            else:
                try:
                    solicitud_form = SolicitudForm(request.POST)
                    material_formset = MaterialFormSet(request.POST, request.FILES, prefix='material')
                    historial_form = HistorialForm(request.POST)

                    if solicitud_form.is_valid() and historial_form.is_valid():
                        id_solicitud = generar_codigo_unico()
                        solicitud = solicitud_form.save(commit=False)
                        solicitud.id_solicitud = id_solicitud
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
                            if solicitud.es_migracion:
                                recipient_list = ['edurazo@ricofarms.com', 'sistemaserp@ricofarms.com', 'erp@ricofarms.com']
                            else:
                                recipient_list = ['compras@ricofarms.com']
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                        return redirect('material')
                    
                except ValueError as e:
                    default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}
                    
                    solicitud_form = SolicitudForm(initial=default_values)
                    material_formset = MaterialFormSet(prefix='material', initial=[{}])

                    return render(request, 'material/material_create.html', {
                        'solicitud_form': solicitud_form, 'material_formset': material_formset, 'error': str(e)
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

            # Si la solicitud está rechazada, el solicitante podrá añadir nuevos elementos
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
                        historial.accion = 'aprobada'
                        action = 'aprobado'
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
                    elif action == 'aprobado':
                        subject = 'Solicitud de material aprobada'
                    else:
                        subject = 'Solicitud de material modificada'

                    # Mensaje
                    if action == 'rechazado':
                        message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/\nComentario: ' + solicitud.comentarios
                    if action == 'aprobado':
                        message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/\n\nMateriales aprobados:' + materialesAprobados + '\n\nServicios aprobados:' + serviciosAprobados
                    else:
                        message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material / servicio, favor de revisar en http://23.19.74.40:8001/materiales/'

                    # Remitente
                    from_email = 'altaproveedoresricofarms@gmail.com'

                    # Destinatario
                    # Si se rechaza la solicitud, se envía un correo al solicitante
                    if action == 'rechazado':
                        recipient_list = [solicitud.usuario.email]
                    # Si se aprueba, se envía un correo al solicitante
                    elif action == 'aprobado':
                        # Si la solicitud contiene algún servicio, se notifica también a contabilidad
                        if notificarContabilidad:
                            recipient_list = [solicitud.usuario.email, 'contadorsr@ricofarms.com']
                        else:
                            recipient_list = [solicitud.usuario.email]
                    else:
                        if request.user.compras:
                            recipient_list = [solicitud.usuario.email, 'edurazo@ricofarms.com', 'sistemaserp@ricofarms.com', 'erp@ricofarms.com']
                        elif request.user.finanzas:
                            recipient_list = [solicitud.usuario.email, 'edurazo@ricofarms.com', 'sistemaserp@ricofarms.com', 'erp@ricofarms.com']
                        elif request.user.sistemas:
                            recipient_list = [solicitud.usuario.email]
                        else:
                            recipient_list = ['compras@ricofarms.com']

                    # Enviar correo
                    #if not solicitud.eliminado:
                        #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                    return redirect('material')

            except ValueError:
                solicitud_form = SolicitudForm(instance=material)
                return render(request, 'material/material_detail.html', {
                    'solicitud': solicitud,
                    'form': solicitud_form,
                    'error': 'Se produjo un error al actualizar, intente de nuevo'
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
    
    if departamento == 'compras':
        email = ['compras@ricofarms.com']
    if departamento == 'finanzas':
        email = ['fiscal@ricofarms.com', 'contabilidadgral@ricofarms.com']
    if departamento == 'sistemas':
        email = ['edurazo@ricofarms.com', 'sistemaserp@ricofarms.com', 'erp@ricofarms.com']

    #send_mail(subject, message, from_email, email, fail_silently=True)

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