from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from .forms import *
from .models import *
from .options import *

import csv
import os

import json
from django.http import JsonResponse

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
            if request.user.compras:
                solicitudes = MaterialSolicitud.objects.filter(pendiente=True)
                if request.user.puede_crear_material:
                    mis_solicitudes = MaterialSolicitud.objects.filter(usuario=request.user)
            elif request.user.finanzas:
                solicitudes = MaterialSolicitud.objects.filter(compras=True)
                if request.user.puede_crear_material:
                    mis_solicitudes = MaterialSolicitud.objects.filter(usuario=request.user)
            elif request.user.sistemas:
                solicitudes = MaterialSolicitud.objects.filter(finanzas=True)
                if request.user.puede_crear_material:
                    mis_solicitudes = MaterialSolicitud.objects.filter(usuario=request.user)
            else:
                solicitudes = MaterialSolicitud.objects.filter(usuario=request.user)
                solicitudes_borradores = solicitudes.filter(borrador=True)
                solicitudes_pendientes = solicitudes.filter(
                    Q(pendiente=True) | 
                    Q(compras=True) | 
                    Q(finanzas=True)
                )
                solicitudes_rechazadas = solicitudes.filter(
                    Q(rechazado_compras=True) | 
                    Q(rechazado_finanzas=True) | 
                    Q(rechazado_sistemas=True)
                )
                solicitudes_aprobadas = solicitudes.filter(sistemas=True)
                solicitudes_eliminadas = solicitudes.filter(eliminado=True)

                historial = []
                for solicitud in solicitudes:
                    historial += MaterialHistorial.objects.filter(id_solicitud=solicitud.id)
                
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

            historial = []
            for solicitud in solicitudes:
                historial += MaterialHistorial.objects.filter(id_solicitud=solicitud.id)

            if request.user.puede_crear_material:
                return render(request, 'material/material.html', {
                    'solicitudes': solicitudes,
                    'mis_solicitudes': mis_solicitudes,
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

                        if solicitud.es_migracion == False:
                            if material_formset.is_valid():
                                for material_form in material_formset:

                                    if not material_form.cleaned_data.get('tipo_alta') or not material_form.cleaned_data.get('subfamilia') or not material_form.cleaned_data.get('nombre_producto') or not material_form.cleaned_data.get('largo') or not material_form.cleaned_data.get('ancho') or not material_form.cleaned_data.get('alto') or not material_form.cleaned_data.get('calibre') or not material_form.cleaned_data.get('unidad_medida'):
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
                        #if not solicitud.borrador:
                        #    subject = 'Nueva solicitud de material'
                        #    message = str(request.user.get_full_name()) + ' ha solicitado un alta de material, favor de revisar en http://23.19.74.40:8001/materiales/'
                        #    from_email = 'altaproveedoresricofarms@gmail.com'
                        #    if solicitud.es_migracion:
                        #        recipient_list = ['edurazo@ricofarms.com']
                        #    else:
                        #        recipient_list = ['compras@ricofarms.com']
                        #    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

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

        if request.method == 'GET':
            default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                            'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}
            if request.user.compras:
                solicitud_form = SolicitudFormForCompras(
                    instance=solicitud, initial=default_values)
                if solicitud.rechazado_compras or solicitud.rechazado_finanzas or solicitud.rechazado_sistemas:
                    materiales = materiales.filter(rechazado=False)
            elif request.user.finanzas:
                solicitud_form = SolicitudFormForFinanzas(
                    instance=solicitud, initial=default_values)
                if solicitud.rechazado_compras or solicitud.rechazado_finanzas or solicitud.rechazado_sistemas:
                    materiales = materiales.filter(rechazado=False)
            elif request.user.sistemas:
                solicitud_form = SolicitudFormForSistemas(
                    instance=solicitud, initial=default_values)
                if solicitud.rechazado_compras or solicitud.rechazado_finanzas or solicitud.rechazado_sistemas:
                    materiales = materiales.filter(rechazado=False)
            else:
                solicitud_form = SolicitudDetailForm(
                    instance=solicitud, initial=default_values)
                if solicitud.rechazado_compras or solicitud.rechazado_finanzas or solicitud.rechazado_sistemas:
                    materiales = materiales.filter(rechazado=True)

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

            return render(request, 'material/material_detail.html', {
                'solicitud': solicitud,
                'solicitud_form': solicitud_form,
                'materiales': materiales,
                'material_forms': material_forms,
                'catalogo_material': catalogo_material,
                'current_user': request.user
            })
        else:
            try:
                if request.user.compras:
                    solicitud_form = SolicitudFormForCompras(
                        request.POST, instance=solicitud)
                    destinatario_correo = [solicitud.usuario.email, 'edurazo@ricofarms.com']
                elif request.user.finanzas:
                    solicitud_form = SolicitudFormForFinanzas(
                        request.POST, instance=solicitud)
                    destinatario_correo = [solicitud.usuario.email, 'edurazo@ricofarms.com']
                elif request.user.sistemas:
                    solicitud_form = SolicitudFormForSistemas(
                        request.POST, instance=solicitud)
                    destinatario_correo = [solicitud.usuario.email]
                else:
                    solicitud_form = SolicitudForm(
                        request.POST, instance=solicitud)
                    destinatario_correo = ['compras@ricofarms.com']

                material_forms = [MaterialForm(
                    request.POST, instance=material, prefix=f'material-{material.id}') for material in materiales]
                
                historial_form = HistorialForm(request.POST)

                if solicitud_form.is_valid() and historial_form.is_valid():
                    solicitud_form.save()

                    if solicitud.es_migracion == False:
                        if all(form.is_valid() for form in material_forms):
                            for form in material_forms:
                                form.save()
                    
                    # Guardar la modificación de la solicitud en el historial de cambios
                    historial = historial_form.save(commit=False)
                    historial.id_solicitud = solicitud.id
                    if solicitud.rechazado_compras or solicitud.rechazado_finanzas or solicitud.rechazado_sistemas:
                        historial.accion = 'rechazada'
                        action = 'rechazado'
                    elif solicitud.pendiente:
                        historial.accion = 'modificada'
                        action = 'modificado'
                    else:
                        historial.accion = 'aprobada'
                        action = 'abrobado'
                    historial.usuario = request.user
                    historial.save()

                    # Enviar correo electrónico
                    #subject = 'Solicitud de material modificada'
                    #if action == 'rechazado':
                    #    message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material, favor de revisar en http://23.19.74.40:8001/materiales/\nComentario: ' + solicitud.comentarios
                    #else:
                    #    message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de material, favor de revisar en http://23.19.74.40:8001/materiales/'
                    #from_email = 'altaproveedoresricofarms@gmail.com'
                    #if action == 'rechazado':
                    #    recipient_list = [solicitud.usuario.email]
                    #else:
                    #    recipient_list = destinatario_correo
                    #send_mail(subject, message, from_email, recipient_list, fail_silently=False)

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
