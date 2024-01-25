from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
import json
from django.http import JsonResponse
from threading import Timer
from datetime import datetime, time
from .forms import *
from .models import *

# VISTA DE INICIO
# Decorador para obligar a iniciar sesión. La ruta a la que devuelve está definida en settings.py
@login_required
def home(request):
    return render(request, 'home.html', {
        'current_user': request.user,
    })

# VISTAS DE CONFIGURACIÓN
@login_required
def settings(request):
    if request.user.compras or request.user.finanzas or request.user.sistemas:
        return render(request, 'settings/settings.html', {
            'current_user': request.user,
        })
    else:
        return redirect('home')

@login_required
def permissions(request):
    try:
        if request.user.compras or request.user.finanzas or request.user.sistemas:
            # Obtener la lista de autorizadores
            autorizadores = CustomUser.objects.filter(
                Q(autorizador = True) |
                Q(autorizador_sustituto = True)
            ).order_by('first_name')

            if request.method == 'GET':
                return render(request, 'settings/permissions.html', {
                    'current_user': request.user,
                    'autorizadores': autorizadores,
                })
            elif request.method == 'POST':
                try:
                    for autorizador in autorizadores:
                        usuario = get_object_or_404(CustomUser, pk=autorizador.id)
                        if autorizador.autorizador_sustituto and request.POST.get(str(autorizador.id)):
                            if request.user.compras:
                                usuario.compras = True
                            if request.user.finanzas:
                                usuario.finanzas = True
                            if request.user.sistemas:
                                usuario.sistemas = True

                            # Enviar correo electrónico al usuario para notificarle los cambios
                            subject = 'Se han actualizado sus permisos de autorización'
                            message =  'El usuario ' + str(request.user.get_full_name()) + ' le ha otorgado permisos para autorizar solicitudes de altas'
                            from_email = 'altaproveedoresricofarms@gmail.com'
                            recipient_list = [autorizador.email]
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                        elif autorizador.autorizador_sustituto and not request.POST.get(str(autorizador.id)):
                            if request.user.compras:
                                usuario.compras = False
                            if request.user.finanzas:
                                usuario.finanzas = False
                            if request.user.sistemas:
                                usuario.sistemas = False

                        usuario.save()
                    return redirect('home')
                    
                except ValueError as e:
                    return render(request, 'settings/permissions.html', {
                        'current_user': request.user,
                        'autorizadores': autorizadores,
                        'error': str(e)
                    })
            else:
                return redirect('home')

        else:
            return redirect('home')
    
    except Exception as e:
        print(f"Se produjo un error al ceder los permisos de autorización: {str(e)}")
        return redirect('home')


# VISTAS DE PROVEEDOR
@login_required
def proveedor(request, tipo):
    try:
        if tipo == 'proveedores' and request.user.puede_crear_proveedor or tipo == 'clientes' and request.user.puede_crear_cliente or request.user.compras or request.user.finanzas or request.user.sistemas:
            
            # Si el usuario es administrador, podrá ver una lista con TODAS las solicitudes
            if request.user.is_superuser:
                if tipo == 'proveedores':
                    all_proveedores = Proveedor.objects.filter(
                        Q(tipo_alta='Proveedor') |
                        Q(tipo_alta='', usuario__puede_crear_proveedor=True)
                    ).order_by('id')
                if tipo == 'clientes':
                    all_proveedores = Proveedor.objects.filter(
                        Q(tipo_alta='Cliente') |
                        Q(tipo_alta='', usuario__puede_crear_cliente=True)
                    ).order_by('id')
            
            # Inicializar la lista de mis_proveedores
            mis_proveedores = []
            
            if request.user.compras:
                if tipo == 'proveedores':
                    proveedores = Proveedor.objects.filter(
                        Q(pendiente=True, tipo_alta='Proveedor') |
                        Q(pendiente=True, tipo_alta='')
                    ).order_by('id')
                    if request.user.puede_crear_proveedor:
                        mis_proveedores = Proveedor.objects.filter(
                            Q(usuario=request.user, tipo_alta='Proveedor') |
                            Q(usuario=request.user, tipo_alta='')
                        ).order_by('id')
                elif tipo == 'clientes':
                    proveedores = Proveedor.objects.filter(
                        Q(pendiente=True, tipo_alta='Cliente') |
                        Q(pendiente=True, tipo_alta='')
                    ).order_by('id')
                    if request.user.puede_crear_cliente:
                        mis_proveedores = Proveedor.objects.filter(
                            Q(usuario=request.user, tipo_alta='Cliente') |
                            Q(usuario=request.user, tipo_alta='')
                        ).order_by('id')
            elif request.user.finanzas:
                if tipo == 'proveedores':
                    proveedores = Proveedor.objects.filter(
                        Q(compras=True, tipo_alta='Proveedor') |
                        Q(compras=True, tipo_alta='')
                    ).order_by('id')
                    if request.user.puede_crear_proveedor:
                        mis_proveedores = Proveedor.objects.filter(
                            Q(usuario=request.user, tipo_alta='Proveedor') |
                            Q(usuario=request.user, tipo_alta='')
                        ).order_by('id')
                elif tipo == 'clientes':
                    proveedores = Proveedor.objects.filter(
                        Q(compras=True, tipo_alta='Cliente') |
                        Q(compras=True, tipo_alta='')
                    ).order_by('id')
                    if request.user.puede_crear_cliente:
                        mis_proveedores = Proveedor.objects.filter(
                            Q(usuario=request.user, tipo_alta='Cliente') |
                            Q(usuario=request.user, tipo_alta='')
                        ).order_by('id')
            elif request.user.sistemas:
                if tipo == 'proveedores':
                    proveedores = Proveedor.objects.filter(
                        Q(finanzas=True, tipo_alta='Proveedor') |
                        Q(finanzas=True, tipo_alta='')
                    ).order_by('id')
                    if request.user.puede_crear_proveedor:
                        mis_proveedores = Proveedor.objects.filter(
                            Q(usuario=request.user, tipo_alta='Proveedor') |
                            Q(usuario=request.user, tipo_alta='')
                        ).order_by('id')
                elif tipo == 'clientes':
                    proveedores = Proveedor.objects.filter(
                        Q(finanzas=True, tipo_alta='Cliente') |
                        Q(finanzas=True, tipo_alta='')
                    ).order_by('id')
                    if request.user.puede_crear_cliente:
                        mis_proveedores = Proveedor.objects.filter(
                            Q(usuario=request.user, tipo_alta='Cliente') |
                            Q(usuario=request.user, tipo_alta='')
                        ).order_by('id')
            else:
                if tipo == 'proveedores':
                    proveedores = Proveedor.objects.filter(
                        Q(usuario=request.user, tipo_alta='Proveedor') |
                        Q(usuario=request.user, tipo_alta='')
                    ).order_by('id')
                elif tipo == 'clientes':
                    proveedores = Proveedor.objects.filter(
                        Q(usuario=request.user, tipo_alta='Cliente') |
                        Q(usuario=request.user, tipo_alta='')
                    ).order_by('id')
                proveedores_borradores = proveedores.filter(borrador=True).order_by('id')
                proveedores_pendientes = proveedores.filter(
                    Q(pendiente=True) | 
                    Q(compras=True) | 
                    Q(finanzas=True)
                ).order_by('id')
                proveedores_rechazados = proveedores.filter(
                    Q(rechazado_compras=True) | 
                    Q(rechazado_finanzas=True) | 
                    Q(rechazado_sistemas=True)
                ).order_by('id')
                proveedores_aprobados = proveedores.filter(sistemas=True).order_by('id')
                proveedores_eliminados = proveedores.filter(eliminado=True).order_by('id')

                historial = []
                for proveedor in proveedores:
                    historial += ProveedorHistorial.objects.filter(id_proveedor=proveedor.id).order_by('id')
                
                return render(request, 'proveedor/proveedor.html', {
                    'tipo': tipo,
                    'proveedores': proveedores,
                    'historial': historial,
                    'proveedores_borradores': proveedores_borradores,
                    'proveedores_pendientes': proveedores_pendientes,
                    'proveedores_rechazados': proveedores_rechazados,
                    'proveedores_aprobados': proveedores_aprobados,
                    'proveedores_eliminados': proveedores_eliminados,
                    'current_user': request.user
                })

            # Si el usuario es autorizador y puede crear solicitudes, incluir las listas para los filtros
            if tipo == 'proveedores' and request.user.puede_crear_proveedor or tipo == 'clientes' and request.user.puede_crear_cliente:
                proveedores_borradores = mis_proveedores.filter(borrador=True).order_by('id')
                proveedores_pendientes = mis_proveedores.filter(
                    Q(pendiente=True) | 
                    Q(compras=True) | 
                    Q(finanzas=True)
                ).order_by('id')
                proveedores_rechazados = mis_proveedores.filter(
                    Q(rechazado_compras=True) | 
                    Q(rechazado_finanzas=True) | 
                    Q(rechazado_sistemas=True)
                ).order_by('id')
                proveedores_aprobados = mis_proveedores.filter(sistemas=True).order_by('id')
                proveedores_eliminados = mis_proveedores.filter(eliminado=True).order_by('id')

            historial = []
            if request.user.is_superuser:
                historial = ProveedorHistorial.objects.all()
            else:
                for proveedor in proveedores:
                    if proveedor not in mis_proveedores:
                        historial += ProveedorHistorial.objects.filter(id_proveedor=proveedor.id).order_by('id')
                for proveedor in mis_proveedores:
                    historial += ProveedorHistorial.objects.filter(id_proveedor=proveedor.id).order_by('id')

            if tipo == 'proveedores' and request.user.puede_crear_proveedor or tipo == 'clientes' and request.user.puede_crear_cliente:
                if request.user.is_superuser:
                    return render(request, 'proveedor/proveedor.html', {
                        'tipo': tipo,
                        'proveedores': proveedores,
                        'mis_proveedores': mis_proveedores,
                        'proveedores_borradores': proveedores_borradores,
                        'proveedores_pendientes': proveedores_pendientes,
                        'proveedores_rechazados': proveedores_rechazados,
                        'proveedores_aprobados': proveedores_aprobados,
                        'proveedores_eliminados': proveedores_eliminados,
                        'all_proveedores': all_proveedores,
                        'historial': historial,
                        'current_user': request.user
                    })
                else:
                    return render(request, 'proveedor/proveedor.html', {
                        'tipo': tipo,
                        'proveedores': proveedores,
                        'mis_proveedores': mis_proveedores,
                        'proveedores_borradores': proveedores_borradores,
                        'proveedores_pendientes': proveedores_pendientes,
                        'proveedores_rechazados': proveedores_rechazados,
                        'proveedores_aprobados': proveedores_aprobados,
                        'proveedores_eliminados': proveedores_eliminados,
                        'historial': historial,
                        'current_user': request.user
                    })
            else:
                if request.user.is_superuser:
                    return render(request, 'proveedor/proveedor.html', {
                        'tipo': tipo,
                        'proveedores': proveedores,
                        'all_proveedores': all_proveedores,
                        'historial': historial,
                        'current_user': request.user
                    })
                else:
                    return render(request, 'proveedor/proveedor.html', {
                        'tipo': tipo,
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
def proveedor_create(request, tipo):
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
                    'tipo': tipo,
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
                        if not proveedor.borrador:
                            # Asunto
                            subject = 'Nueva solicitud de proveedor'

                            # Mensaje
                            if proveedor.tipo_alta == 'Proveedor':
                                message = str(request.user.get_full_name()) + ' ha solicitado un alta de proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/'
                            elif proveedor.tipo_alta == 'Cliente':
                                message = str(request.user.get_full_name()) + ' ha solicitado un alta de cliente, favor de revisar en http://23.19.74.40:8001/clientes/'
                            else:
                                message = str(request.user.get_full_name()) + ' ha solicitado un alta de cliente / proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/'
                            
                            # Remitente
                            from_email = 'altaproveedoresricofarms@gmail.com'

                            # Destinatario
                            recipient_list = []
                            if proveedor.es_migracion:
                                autorizadores = CustomUser.objects.filter(sistemas = True)
                            elif proveedor.tipo_alta == 'Cliente':
                                autorizadores = CustomUser.objects.filter(finanzas = True)
                            else:
                                autorizadores = CustomUser.objects.filter(compras = True)

                            for autorizador in autorizadores:
                                recipient_list.append(autorizador.email)

                            # Enviar correo
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                        return redirect('proveedor')
                    
                except ValueError as e:
                    default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}

                    return render(request, 'proveedor/proveedor_create.html', {
                        'form': ProveedorForm(initial=default_values),
                        'error': str(e),
                        'current_user': request.user,
                    })
        else:
            return redirect('home')
    
    except Exception as e:
        print(f"Se produjo un error al crear el proveedor: {str(e)}")
        return redirect('home')


@login_required
def proveedor_detail(request, proveedor_id):
    try:
        if request.user.puede_crear_proveedor or request.user.puede_crear_cliente or request.user.compras or request.user.finanzas or request.user.sistemas:
            proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

            if request.method == 'GET':
                default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                                'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False, 'borrador': False}
                if proveedor.usuario.id == request.user.id:
                    proveedor_form = ProveedorDetailForm(
                        instance=proveedor, initial=default_values)
                elif proveedor.pendiente and request.user.compras:
                    proveedor_form = ProveedorFormForCompras(
                        instance=proveedor, initial=default_values)
                elif proveedor.compras and request.user.finanzas:
                    proveedor_form = ProveedorFormForFinanzas(
                        instance=proveedor, initial=default_values)
                elif proveedor.finanzas and request.user.sistemas:
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
                    if proveedor.usuario.id == request.user.id:
                        proveedor_form = ProveedorDetailForm(
                            request.POST, request.FILES, instance=proveedor)
                    elif proveedor.pendiente and request.user.compras:
                        proveedor_form = ProveedorFormForCompras(
                            request.POST, instance=proveedor)
                    elif proveedor.compras and request.user.finanzas:
                        proveedor_form = ProveedorFormForFinanzas(
                            request.POST, instance=proveedor)
                    elif proveedor.finanzas and request.user.sistemas:
                        proveedor_form = ProveedorFormForSistemas(
                            request.POST, instance=proveedor)
                    else:
                        proveedor_form = ProveedorDetailForm(
                            request.POST, request.FILES, instance=proveedor)
                    
                    historial_form = HistorialForm(request.POST)
                                
                    if proveedor_form.is_valid() and historial_form.is_valid():
                        proveedor_form.save()
                        
                        # Guardar la modificación de la solicitud en el historial de cambios
                        historial = historial_form.save(commit=False)
                        historial.id_proveedor = proveedor.id
                        if proveedor.rechazado_compras or proveedor.rechazado_finanzas or proveedor.rechazado_sistemas:
                            historial.accion = 'rechazada'
                            action = 'rechazado'
                        elif proveedor.pendiente or proveedor.compras or proveedor.finanzas:
                            historial.accion = 'modificada'
                            action = 'modificado'
                        elif proveedor.eliminado:
                            historial.accion = 'eliminada'
                            action = 'eliminado'
                        elif proveedor.sistemas:
                            historial.accion = 'registrada'
                            action = 'registrado'
                        historial.usuario = request.user
                        historial.save()

                        # Enviar correo electrónico
                        # Asunto
                        subject = 'Solicitud de proveedor modificada'

                        # Mensaje
                        if action == 'rechazado':
                            if proveedor.tipo_alta == 'Proveedor':
                                message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de proveedor con RFC ' + proveedor.rfc if proveedor.rfc != '' else proveedor.rfc_migracion + ', favor de revisar en http://23.19.74.40:8001/proveedores/\nComentario: ' + proveedor.comentarios
                            elif proveedor.tipo_alta == 'Cliente':
                                message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de cliente con RFC ' + proveedor.rfc if proveedor.rfc != '' else proveedor.rfc_migracion + ', favor de revisar en http://23.19.74.40:8001/clientes/\nComentario: ' + proveedor.comentarios
                            else:
                                message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de cliente / proveedor con RFC ' + proveedor.rfc if proveedor.rfc != '' else proveedor.rfc_migracion + ', favor de revisar en http://23.19.74.40:8001/proveedores/\nComentario: ' + proveedor.comentarios
                        else:
                            if proveedor.tipo_alta == 'Proveedor':
                                message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de proveedor con RFC ' + proveedor.rfc if proveedor.rfc != '' else proveedor.rfc_migracion + ', favor de revisar en http://23.19.74.40:8001/proveedores/'
                            elif proveedor.tipo_alta == 'Cliente':
                                message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de cliente con RFC ' + proveedor.rfc if proveedor.rfc != '' else proveedor.rfc_migracion + ', favor de revisar en http://23.19.74.40:8001/clientes/'
                            else:
                                message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de cliente / proveedor con RFC ' + proveedor.rfc if proveedor.rfc != '' else proveedor.rfc_migracion + ', favor de revisar en http://23.19.74.40:8001/proveedores/'

                        # Remitente
                        from_email = 'altaproveedoresricofarms@gmail.com'

                        # Destinatario
                        recipient_list = [proveedor.usuario.email]
                        # Si se registra un proveedor en Agrosmart, se notifica a contabilidad
                        if action == 'registrado' and proveedor.tipo_alta == 'Proveedor':
                            recipient_list.append('contadorsr@ricofarms.com')
                        # Si se aprueba, se manda correo al solicitante y al siguiente aprobador
                        elif action != 'rechazado':
                            if request.user.compras:
                                autorizadores = CustomUser.objects.filter(finanzas = True)
                            elif request.user.finanzas:
                                autorizadores = CustomUser.objects.filter(sistemas = True)
                            elif not request.user.sistemas:
                                recipient_list = []
                                autorizadores = CustomUser.objects.filter(compras = True)
                            for autorizador in autorizadores:
                                recipient_list.append(autorizador.email)

                        # Enviar correo
                        #if not proveedor.eliminado:
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                        return redirect('proveedor')
                    
                except ValueError:
                    proveedor_form = ProveedorDetailForm(instance=proveedor)
                    return render(request, 'proveedor/proveedor_detail.html', {
                        'proveedor': proveedor,
                        'form': proveedor_form,
                        'error': 'Se produjo un error al actualizar, intente de nuevo',
                        'current_user': request.user,
                    })
        else:
            return redirect('home')
    
    except Exception as e:
        print(f"Se produjo un error al cargar el proveedor: {str(e)}")
        return redirect('home')


# ENVIANDO UN CORREO DE RECORDATORIO CADA 30 MINUTOS

def enviarCorreo(departamento, elementos, clientes, proveedores):
    cadenaClientes = ''
    cadenaProveedores = ''

    for cliente in clientes:
        cadenaClientes += '\n' + cliente
        
    for proveedor in proveedores:
        cadenaProveedores += '\n' + proveedor

    subject = 'Recordatorio de solicitudes por aprobar'
    message = 'Tiene ' + str(elementos) + ' solicitudes de alta de cliente / proveedor pendientes de aprobación. Por favor ingrese a http://23.19.74.40:8001/proveedores/ para revisarlas.' + cadenaClientes if len(clientes) > 0 else '' + cadenaProveedores if len(proveedores) > 0 else ''

    from_email = 'altaproveedoresricofarms@gmail.com'
    
    recipient_list = []
    if departamento == 'compras':
        autorizadores = CustomUser.objects.filter(compras = True)
    elif departamento == 'finanzas':
        autorizadores = CustomUser.objects.filter(finanzas = True)
    elif departamento == 'sistemas':
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

        # Revisar si hay solicitudes de cliente / proveedor pendientes de aprobar por compras
        proveedores_compras = Proveedor.objects.filter(pendiente=True)
        if len(proveedores_compras) > 0:
            clientes = []
            proveedores = []
            for proveedor in proveedores_compras:
                if proveedor.tipo_alta == 'Cliente':
                    if proveedor.rfc != '':
                        clientes.append(str(proveedor.id) + ' - ' + proveedor.rfc)
                    else:
                        clientes.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)
                if proveedor.tipo_alta == 'Proveedor':
                    if proveedor.rfc != '':
                        proveedores.append(str(proveedor.id) + ' - ' + proveedor.rfc)
                    else:
                        proveedores.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)

            enviarCorreo('compras', len(proveedores_compras), clientes, proveedores)

        # Revisar si hay solicitudes de cliente / proveedor pendientes de aprobar por finanzas
        proveedores_finanzas = Proveedor.objects.filter(compras=True)
        if len(proveedores_finanzas) > 0:
            clientes = []
            proveedores = []
            for proveedor in proveedores_finanzas:
                if proveedor.tipo_alta == 'Cliente':
                    if proveedor.rfc != '':
                        clientes.append(str(proveedor.id) + ' - ' + proveedor.rfc)
                    else:
                        clientes.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)
                if proveedor.tipo_alta == 'Proveedor':
                    if proveedor.rfc != '':
                        proveedores.append(str(proveedor.id) + ' - ' + proveedor.rfc)
                    else:
                        proveedores.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)

            enviarCorreo('finanzas', len(proveedores_finanzas), clientes, proveedores)

        # Revisar si hay solicitudes de cliente / proveedor pendientes de aprobar por sistemas
        proveedores_sistemas = Proveedor.objects.filter(finanzas=True)
        if len(proveedores_sistemas) > 0:
            clientes = []
            proveedores = []
            for proveedor in proveedores_sistemas:
                if proveedor.tipo_alta == 'Cliente':
                    if proveedor.rfc != '':
                        clientes.append(str(proveedor.id) + ' - ' + proveedor.rfc)
                    else:
                        clientes.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)
                if proveedor.tipo_alta == 'Proveedor':
                    if proveedor.rfc != '':
                        proveedores.append(str(proveedor.id) + ' - ' + proveedor.rfc)
                    else:
                        proveedores.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)

            enviarCorreo('sistemas', len(proveedores_sistemas), clientes, proveedores)

    # El correo de recordatorio debe enviarse cada 2 horas
    Timer(7200, solicitudesPendientes).start()

#solicitudesPendientes()