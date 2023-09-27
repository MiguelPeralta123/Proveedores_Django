from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import *
from .models import Proveedor

# VISTA DE INICIO
# Decorator to force login. The return route is defined in proveedores/settings.py
@login_required
def home(request):
    return render(request, 'home.html')


# VISTAS DE PROVEEDOR (GET ALL, CREATE, DETAIL)

@login_required
def proveedor(request):
    if request.user.compras:
        proveedores = Proveedor.objects.filter(pendiente=True, eliminado=False)
    elif request.user.finanzas:
        proveedores = Proveedor.objects.filter(compras=True, eliminado=False)
    elif request.user.sistemas:
        proveedores = Proveedor.objects.filter(finanzas=True, eliminado=False)
    else:
        proveedores = Proveedor.objects.filter(usuario=request.user, eliminado=False)

    historial = []
    for proveedor in proveedores:
        historial += ProveedorHistorial.objects.filter(id_proveedor=proveedor.id)

    return render(request, 'proveedor/proveedor.html', {
        'proveedores': proveedores,
        'historial': historial
    })


@login_required
def proveedor_create(request):
    if request.user.puede_comprar:
        if request.method == 'GET':
            default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                              'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False}

            return render(request, 'proveedor/proveedor_create.html', {
                'form': ProveedorForm(initial=default_values)
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
                    subject = 'Nueva solicitud de proveedor'
                    message = str(request.user.get_full_name()) + ' ha solicitado un alta de proveedor, favor de revisar en http://127.0.0.1:8000/proveedores/'
                    from_email = 'altaproveedoresricofarms@gmail.com'
                    if proveedor.es_migracion:
                        recipient_list = ['l18330484@hermosillo.tecnm.mx']
                    else:
                        recipient_list = ['maikperalta123@gmail.com']
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                    return redirect('proveedor')
                
            except ValueError as e:
                default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                              'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False}

                return render(request, 'proveedor/proveedor_create.html', {
                    'form': ProveedorForm(initial=default_values),
                    'error': str(e)
                })
    else:
        return redirect('proveedor')


@login_required
def proveedor_detail(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if request.method == 'GET':
        default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                          'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False}
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
            
        return render(request, 'proveedor/proveedor_detail.html', {
            'proveedor': proveedor,
            'form': proveedor_form,
            'current_user': request.user
        })
    else:
        try:
            if request.user.compras:
                proveedor_form = ProveedorFormForCompras(
                    request.POST, instance=proveedor)
                destinatario_correo = [proveedor.usuario.email, 'maikperalta248@gmail.com']
            elif request.user.finanzas:
                proveedor_form = ProveedorFormForFinanzas(
                    request.POST, instance=proveedor)
                destinatario_correo = [proveedor.usuario.email, 'l18330484@hermosillo.tecnm.mx']
            elif request.user.sistemas:
                proveedor_form = ProveedorFormForSistemas(
                    request.POST, instance=proveedor)
                destinatario_correo = [proveedor.usuario.email]
            else:
                proveedor_form = ProveedorDetailForm(
                    request.POST, instance=proveedor)
                destinatario_correo = ['maikperalta123@gmail.com']
            
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
                else:
                    historial.accion = 'aprobada'
                    action = 'abrobado'
                historial.usuario = request.user
                historial.save()

                # Enviar correo electrónico
                subject = 'Solicitud de proveedor modificada'
                message = str(request.user.get_full_name()) + ' ha ' + action + ' un alta de proveedor, favor de revisar en http://127.0.0.1:8000/proveedores/'
                from_email = 'altaproveedoresricofarms@gmail.com'
                if action == 'rechazado':
                    recipient_list = [proveedor.usuario.email]
                else:
                    recipient_list = destinatario_correo
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return redirect('proveedor')
            
        except ValueError:
            proveedor_form = ProveedorDetailForm(instance=proveedor)
            return render(request, 'proveedor/proveedor_detail.html', {
                'proveedor': proveedor,
                'form': proveedor_form,
                'error': 'Se produjo un error al actualizar, intente de nuevo'
            })
