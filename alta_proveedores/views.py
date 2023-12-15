from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
import json
from django.http import JsonResponse
from threading import Timer
from .forms import *
from .models import *

# VISTA DE INICIO
# Decorador para obligar a iniciar sesión. La ruta a la que devuelve está definida en settings.py
@login_required
def home(request):
    return render(request, 'home.html')

# VISTAS DE CONFIGURACIÓN
@login_required
def settings(request):
    if request.user.compras or request.user.finanzas or request.user.sistemas:
        return render(request, 'settings/settings.html')
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
                        elif autorizador.autorizador_sustituto and not request.POST.get(str(autorizador.id)):
                            if request.user.compras:
                                usuario.compras = False
                            if request.user.finanzas:
                                usuario.finanzas = False
                            if request.user.sistemas:
                                usuario.sistemas = False
                        usuario.save()

                        # Enviar correo electrónico al usuario para notificarle los cambios
                        subject = 'Se han actualizado sus permisos de autorización'
                        message =  'El usuario ' + str(request.user.get_full_name()) + ' le ha otorgado permisos para autorizar solicitudes de altas'
                        from_email = 'altaproveedoresricofarms@gmail.com'
                        recipient_list = [autorizador.email]
                        #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

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
                        Q(tipo_alta='')
                    ).order_by('id')
                if tipo == 'clientes':
                    all_proveedores = Proveedor.objects.filter(
                        Q(tipo_alta='Cliente') |
                        Q(tipo_alta='')
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
                        if not proveedor.borrador:
                            subject = 'Nueva solicitud de proveedor'
                            message = str(request.user.get_full_name()) + ' ha solicitado un alta de proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/'
                            from_email = 'altaproveedoresricofarms@gmail.com'
                            if proveedor.es_migracion:
                                recipient_list = ['edurazo@ricofarms.com', 'sistemaserp@ricofarms.com', 'erp@ricofarms.com']
                            elif proveedor.tipo_alta == 'Cliente':
                                recipient_list = ['fiscal@ricofarms.com', 'contabilidadgral@ricofarms.com']
                            else:
                                recipient_list = ['compras@ricofarms.com']
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

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
        if request.user.puede_crear_proveedor or request.user.puede_crear_cliente or request.user.compras or request.user.finanzas or request.user.sistemas:
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
                        destinatario_correo = [proveedor.usuario.email, 'edurazo@ricofarms.com', 'sistemaserp@ricofarms.com', 'erp@ricofarms.com']
                    elif request.user.sistemas:
                        proveedor_form = ProveedorFormForSistemas(
                            request.POST, instance=proveedor)
                        destinatario_correo = [proveedor.usuario.email]
                    else:
                        proveedor_form = ProveedorDetailForm(
                            request.POST, request.FILES, instance=proveedor)
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
                        elif proveedor.pendiente or proveedor.compras or proveedor.finanzas:
                            historial.accion = 'modificada'
                            action = 'modificado'
                        elif proveedor.eliminado:
                            historial.accion = 'eliminada'
                            action = 'eliminado'
                        elif proveedor.sistemas:
                            historial.accion = 'aprobada'
                            action = 'abrobado'
                        historial.usuario = request.user
                        historial.save()

                        # Enviar correo electrónico
                        subject = 'Solicitud de proveedor modificada'
                        if action == 'rechazado':
                            message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/\nComentario: ' + proveedor.comentarios
                        else:
                            message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de proveedor, favor de revisar en http://23.19.74.40:8001/proveedores/'
                        from_email = 'altaproveedoresricofarms@gmail.com'
                        if action == 'rechazado':
                            recipient_list = [proveedor.usuario.email]
                        else:
                            recipient_list = destinatario_correo
                        #if not proveedor.eliminado:
                            #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

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


# ENVIANDO UN CORREO DE RECORDATORIO CADA 30 MINUTOS

def enviarCorreo(departamento, elementos, folios):
    cadenaFolios = ''
    for folio in folios:
        cadenaFolios += '\n' + folio

    subject = 'Recordatorio de solicitudes por aprobar'
    message = 'Tiene ' + str(elementos) + ' solicitudes de alta de proveedor pendientes de aprobación. Por favor ingrese a http://23.19.74.40:8001/proveedores/ para revisarlas.' + cadenaFolios

    from_email = 'altaproveedoresricofarms@gmail.com'
    
    if departamento == 'compras':
        email = ['compras@ricofarms.com']
    if departamento == 'finanzas':
        email = ['fiscal@ricofarms.com', 'contabilidadgral@ricofarms.com']
    if departamento == 'sistemas':
        email = ['edurazo@ricofarms.com', 'sistemaserp@ricofarms.com', 'erp@ricofarms.com']

    #send_mail(subject, message, from_email, email, fail_silently=True)

def solicitudesPendientes():
    # Revisar si hay solicitudes de cliente / proveedor pendientes de aprobar por compras
    proveedores_compras = Proveedor.objects.filter(pendiente=True)
    if len(proveedores_compras) > 0:
        folios = []
        for proveedor in proveedores_compras:
            if proveedor.rfc != '':
                folios.append(str(proveedor.id) + ' - ' + proveedor.rfc)
            else:
                folios.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)
        enviarCorreo('compras', len(proveedores_compras), folios)

    # Revisar si hay solicitudes de cliente / proveedor pendientes de aprobar por finanzas
    proveedores_finanzas = Proveedor.objects.filter(compras=True)
    if len(proveedores_finanzas) > 0:
        folios = []
        for proveedor in proveedores_finanzas:
            if proveedor.rfc != '':
                folios.append(str(proveedor.id) + ' - ' + proveedor.rfc)
            else:
                folios.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)
        enviarCorreo('finanzas', len(proveedores_finanzas), folios)

    # Revisar si hay solicitudes de cliente / proveedor pendientes de aprobar por sistemas
    proveedores_sistemas = Proveedor.objects.filter(finanzas=True)
    if len(proveedores_sistemas) > 0:
        folios = []
        for proveedor in proveedores_sistemas:
            if proveedor.rfc != '':
                folios.append(str(proveedor.id) + ' - ' + proveedor.rfc)
            else:
                folios.append(str(proveedor.id) + ' - ' + proveedor.rfc_migracion)
        enviarCorreo('sistemas', len(proveedores_sistemas), folios)

    Timer(1800, solicitudesPendientes).start()

#solicitudesPendientes()