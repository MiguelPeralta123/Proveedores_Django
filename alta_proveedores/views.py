from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
import time
from .forms import *
from .models import *

import json
from django.http import JsonResponse

# VISTA DE INICIO
# Decorator to force login. The return route is defined in proveedores/settings.py
@login_required
def home(request):
    return render(request, 'home.html')


# VISTAS DE PROVEEDOR (GET ALL, CREATE, DETAIL)

@login_required
def proveedor(request):
    try:
        if request.user.puede_crear_proveedor or request.user.puede_crear_cliente or request.user.compras or request.user.finanzas or request.user.sistemas:
            if request.user.compras:
                proveedores = Proveedor.objects.filter(pendiente=True)
                if request.user.puede_crear_proveedor or request.user.puede_crear_cliente:
                    mis_proveedores = Proveedor.objects.filter(usuario=request.user)
            elif request.user.finanzas:
                proveedores = Proveedor.objects.filter(compras=True)
                if request.user.puede_crear_proveedor or request.user.puede_crear_cliente:
                    mis_proveedores = Proveedor.objects.filter(usuario=request.user)
            elif request.user.sistemas:
                proveedores = Proveedor.objects.filter(finanzas=True)
                if request.user.puede_crear_proveedor or request.user.puede_crear_cliente:
                    mis_proveedores = Proveedor.objects.filter(usuario=request.user)
            else:
                proveedores = Proveedor.objects.filter(usuario=request.user)
                proveedores_borradores = proveedores.filter(borrador=True)
                proveedores_pendientes = proveedores.filter(
                    Q(pendiente=True) | 
                    Q(compras=True) | 
                    Q(finanzas=True)
                )
                proveedores_rechazados = proveedores.filter(
                    Q(rechazado_compras=True) | 
                    Q(rechazado_finanzas=True) | 
                    Q(rechazado_sistemas=True)
                )
                proveedores_aprobados = proveedores.filter(sistemas=True)
                proveedores_eliminados = proveedores.filter(eliminado=True)

                historial = []
                for proveedor in proveedores:
                    historial += ProveedorHistorial.objects.filter(id_proveedor=proveedor.id)
                
                return render(request, 'proveedor/proveedor.html', {
                    'proveedores': proveedores,
                    'historial': historial,
                    'proveedores_borradores': proveedores_borradores,
                    'proveedores_pendientes': proveedores_pendientes,
                    'proveedores_rechazados': proveedores_rechazados,
                    'proveedores_aprobados': proveedores_aprobados,
                    'proveedores_eliminados': proveedores_eliminados,
                    'current_user': request.user
                })

            historial = []
            for proveedor in proveedores:
                historial += ProveedorHistorial.objects.filter(id_proveedor=proveedor.id)

            if request.user.puede_crear_proveedor or request.user.puede_crear_cliente:
                return render(request, 'proveedor/proveedor.html', {
                    'proveedores': proveedores,
                    'mis_proveedores': mis_proveedores,
                    'historial': historial,
                    'current_user': request.user
                })
            else:
                return render(request, 'proveedor/proveedor.html', {
                    'proveedores': proveedores,
                    'historial': historial,
                    'current_user': request.user
                })
        else:
            return redirect('home')

    except Exception as e:
        print(f"Se produjo un error al cargar los proveedores: {str(e)}")
        return redirect('home')


@login_required
def proveedor_create(request):
    try:
        if request.user.puede_crear_proveedor or request.user.puede_crear_cliente:
            if request.method == 'GET':
                default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}

                # Cargando los registros de proveedores desde la base de datos
                #catalogo_proveedor = list(CatalogoProveedor.objects.values())
                #catalogo_proveedor_json = json.dumps(catalogo_proveedor)

                # Cargando los registros de proveedores desde el archivo catalogo_proveedores.csv
                csv_path = os.path.join('csv_files', 'catalogo_proveedores.csv')
                with open(csv_path, 'r') as csv_file:
                    # Lee el archivo CSV
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader) # Skipping headers
                    
                    # Inicializa la lista que contendrá los elementos
                    catalogo_proveedor = []
                    
                    # Itera sobre cada fila del archivo CSV
                    for row in csv_reader:
                        # Extrae la información necesaria de las columnas
                        codigo = row[0]
                        rfc = row[3]
                        nombre_comercial = row[2]
                        
                        # Crea la cadena de texto con el formato deseado
                        formato = f'{rfc} - {nombre_comercial}'
                        
                        # Agrega la tupla a la lista
                        catalogo_proveedor.append({'value': rfc, 'text': formato})
                
                return render(request, 'proveedor/proveedor_create.html', {
                    'form': ProveedorForm(initial=default_values),
                    'catalogo_proveedor': catalogo_proveedor,
                    'current_user': request.user,
                })
            else:
                try:
                    proveedor_form = ProveedorForm(request.POST, request.FILES)
                    historial_form = HistorialForm(request.POST)

                    if proveedor_form.is_valid() and historial_form.is_valid():
                        proveedor = proveedor_form.save(commit=False)
                        proveedor.usuario = request.user
                        proveedor.save()
                        
                        # Guardar la creacion de la solicitud en el historial de cambios
                        historial = historial_form.save(commit=False)
                        historial.id_proveedor = proveedor.id
                        historial.accion = 'creada'
                        historial.usuario = request.user
                        historial.save()

                        # Enviar correo electrónico
                        #if not proveedor.borrador:
                        #    subject = 'Nueva solicitud de proveedor'
                        #    message = str(request.user.get_full_name()) + ' ha solicitado un alta de proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/'
                        #    from_email = 'altaproveedoresricofarms@gmail.com'
                        #    if proveedor.es_migracion:
                        #        recipient_list = ['edurazo@ricofarms.com']
                        #    elif proveedor.tipo_alta == 'Cliente':
                        #        recipient_list = ['fiscal@ricofarms.com', 'contabilidadgral@ricofarms.com']
                        #    else:
                        #        recipient_list = ['compras@ricofarms.com']
                        #    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                        return redirect('proveedor')
                    
                except ValueError as e:
                    default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}

                    return render(request, 'proveedor/proveedor_create.html', {
                        'form': ProveedorForm(initial=default_values),
                        'error': str(e)
                    })
        else:
            return redirect('home')
    
    except Exception as e:
        print(f"Se produjo un error al crear el proveedor: {str(e)}")
        return redirect('home')


@login_required
def proveedor_detail(request, proveedor_id):
    try:
        if request.user.puede_crear_proveedor or request.user.puede_crear_cliente:
            proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

            if request.method == 'GET':
                default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}
                if request.user.compras:
                    proveedor_form = ProveedorFormForCompras(
                        instance=proveedor, initial=default_values)
                elif request.user.finanzas:
                    proveedor_form = ProveedorFormForFinanzas(
                        instance=proveedor, initial=default_values)
                elif request.user.sistemas:
                    proveedor_form = ProveedorFormForSistemas(
                        instance=proveedor, initial=default_values)
                else:
                    proveedor_form = ProveedorDetailForm(
                        instance=proveedor, initial=default_values)
                
                # Cargando los registros de proveedores desde la base de datos
                #catalogo_proveedor = list(CatalogoProveedor.objects.values())
                #catalogo_proveedor_json = json.dumps(catalogo_proveedor)

                # Cargando los registros de proveedores desde el archivo catalogo_proveedores.csv
                csv_path = os.path.join('csv_files', 'catalogo_proveedores.csv')
                with open(csv_path, 'r') as csv_file:
                    # Lee el archivo CSV
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader) # Skipping headers
                    
                    # Inicializa la lista que contendrá las tuplas
                    catalogo_proveedor = []
                    
                    # Itera sobre cada fila del archivo CSV
                    for row in csv_reader:
                        # Extrae la información necesaria de las columnas
                        codigo = row[0]
                        rfc = row[3]
                        nombre_comercial = row[2]
                        
                        # Crea la cadena de texto con el formato deseado
                        formato = f'{rfc} - {nombre_comercial}'
                        
                        # Agrega la tupla a la lista
                        catalogo_proveedor.append({'value': rfc, 'text': formato})
                    
                return render(request, 'proveedor/proveedor_detail.html', {
                    'proveedor': proveedor,
                    'form': proveedor_form,
                    'catalogo_proveedor': catalogo_proveedor,
                    'current_user': request.user,
                })
            else:
                try:
                    if request.user.compras:
                        proveedor_form = ProveedorFormForCompras(
                            request.POST, instance=proveedor)
                        destinatario_correo = [proveedor.usuario.email, 'fiscal@ricofarms.com', 'contabilidadgral@ricofarms.com']
                    elif request.user.finanzas:
                        proveedor_form = ProveedorFormForFinanzas(
                            request.POST, instance=proveedor)
                        destinatario_correo = [proveedor.usuario.email, 'edurazo@ricofarms.com']
                    elif request.user.sistemas:
                        proveedor_form = ProveedorFormForSistemas(
                            request.POST, instance=proveedor)
                        destinatario_correo = [proveedor.usuario.email]
                    else:
                        proveedor_form = ProveedorDetailForm(
                            request.POST, instance=proveedor)
                        destinatario_correo = ['compras@ricofarms.com']
                    
                    historial_form = HistorialForm(request.POST)
                                
                    if proveedor_form.is_valid() and historial_form.is_valid():
                        proveedor_form.save()
                        
                        # Guardar la modificación de la solicitud en el historial de cambios
                        historial = historial_form.save(commit=False)
                        historial.id_proveedor = proveedor.id
                        if proveedor.rechazado_compras or proveedor.rechazado_finanzas or proveedor.rechazado_sistemas:
                            historial.accion = 'rechazada'
                            action = 'rechazado'
                        elif proveedor.pendiente:
                            historial.accion = 'modificada'
                            action = 'modificado'
                        elif proveedor.eliminado:
                            historial.accion = 'eliminada'
                            action = 'eliminado'
                        else:
                            historial.accion = 'aprobada'
                            action = 'abrobado'
                        historial.usuario = request.user
                        historial.save()

                        # Enviar correo electrónico
                        #subject = 'Solicitud de proveedor modificada'
                        #if action == 'rechazado':
                        #    message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/\nComentario: ' + proveedor.comentarios
                        #else:
                        #    message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/'
                        #from_email = 'altaproveedoresricofarms@gmail.com'
                        #if action == 'rechazado':
                        #    recipient_list = [proveedor.usuario.email]
                        #else:
                        #    recipient_list = destinatario_correo
                        #if not proveedor.eliminado:
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                        return redirect('proveedor')
                    
                except ValueError:
                    proveedor_form = ProveedorDetailForm(instance=proveedor)
                    return render(request, 'proveedor/proveedor_detail.html', {
                        'proveedor': proveedor,
                        'form': proveedor_form,
                        'error': 'Se produjo un error al actualizar, intente de nuevo'
                    })
        else:
            return redirect('home')
    
    except Exception as e:
        print(f"Se produjo un error al cargar el proveedor: {str(e)}")
        return redirect('home')

# Función que se ejecuta cada 2 minutos
#def mi_funcion():
    # Coloca el código de tu función aquí
#    print("Ejecutando mi función cada 2 minutos")

#while True:
#    mi_funcion()  # Llama a tu función
#    time.sleep(120)