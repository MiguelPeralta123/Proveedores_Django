from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Proveedor
from django.contrib.auth.decorators import login_required

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
            elif request.user.finanzas:
                proveedor_form = ProveedorFormForFinanzas(
                    request.POST, instance=proveedor)
            elif request.user.sistemas:
                proveedor_form = ProveedorFormForSistemas(
                    request.POST, instance=proveedor)
            else:
                proveedor_form = ProveedorDetailForm(
                    request.POST, instance=proveedor)
            
            historial_form = HistorialForm(request.POST)
                        
            if proveedor_form.is_valid() and historial_form.is_valid():
                proveedor_form.save()
                
                # Guardar la modificación de la solicitud en el historial de cambios
                historial = historial_form.save(commit=False)
                historial.id_proveedor = proveedor.id
                if proveedor.rechazado_compras or proveedor.rechazado_finanzas or proveedor.rechazado_sistemas:
                    historial.accion = 'rechazada'
                elif proveedor.pendiente:
                    historial.accion = 'modificada'
                else:
                    historial.accion = 'aprobada'
                historial.usuario = request.user
                historial.save()

                return redirect('proveedor')
            
        except ValueError:
            proveedor_form = ProveedorDetailForm(instance=proveedor)
            return render(request, 'proveedor/proveedor_detail.html', {
                'proveedor': proveedor,
                'form': proveedor_form,
                'error': 'Se produjo un error al actualizar, intente de nuevo'
            })
