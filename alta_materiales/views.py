from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .forms import *
from .models import MaterialSolicitud, Material, MaterialHistorial
from django.contrib.auth.decorators import login_required
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
    # Compras, finanzas y sistemas pueden ver las solicitudes de todos los usuarios
    if request.user.compras:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por compras
        solicitudes = MaterialSolicitud.objects.filter(pendiente=True, eliminado=False)
    elif request.user.finanzas:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por finanzas
        solicitudes = MaterialSolicitud.objects.filter(compras=True, eliminado=False)
    elif request.user.sistemas:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por sistemas
        solicitudes = MaterialSolicitud.objects.filter(finanzas=True, eliminado=False)
    else:
        # Trayendo de la base de datos las solicitudes que correspondan al usuario logueado
        solicitudes = MaterialSolicitud.objects.filter(usuario=request.user, eliminado=False)

    historial = []
    for solicitud in solicitudes:
        historial += MaterialHistorial.objects.filter(id_solicitud=solicitud.id)

    return render(request, 'material/material.html', {
        'solicitudes': solicitudes,
        'historial': historial
    })


@login_required
def material_create(request):
    if request.user.puede_comprar:
        MaterialFormSet = formset_factory(MaterialForm, extra=0)

        if request.method == 'GET':
            default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                              'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False}

            solicitud_form = SolicitudForm(initial=default_values)
            material_formset = MaterialFormSet(prefix='material', initial=[{}])

            return render(request, 'material/material_create.html', {
                'solicitud_form': solicitud_form,
                'material_formset': material_formset
            })
        
        else:
            try:
                solicitud_form = SolicitudForm(request.POST)
                material_formset = MaterialFormSet(request.POST, prefix='material')
                historial_form = HistorialForm(request.POST)

                if solicitud_form.is_valid() and material_formset.is_valid() and historial_form.is_valid():
                    id_solicitud = generar_codigo_unico()
                    solicitud = solicitud_form.save(commit=False)
                    solicitud.id_solicitud = id_solicitud
                    solicitud.usuario = request.user
                    solicitud.save()

                    for material_form in material_formset:
                        if not material_form.cleaned_data.get('nombre_producto'):
                            continue  # Saltar formularios con nombre_producto vacío
                        material = material_form.save(commit=False)
                        material.id_solicitud = id_solicitud
                        material.save()
                    
                    # Guardar la creacion de la solicitud en el historial de cambios
                    historial = historial_form.save(commit=False)
                    historial.id_solicitud = solicitud.id
                    historial.accion = 'creada'
                    historial.usuario = request.user
                    historial.save()
                    return redirect('material')
            except ValueError as e:
                default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                              'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False}
                
                solicitud_form = SolicitudForm(initial=default_values)
                material_formset = MaterialFormSet(prefix='material', initial=[{}])

                return render(request, 'material/material_create.html', {
                    'solicitud_form': solicitud_form, 'material_formset': material_formset, 'error': str(e)
                })
    else:
        return redirect('material')


@login_required
def material_detail(request, material_id):
    solicitud = get_object_or_404(MaterialSolicitud, pk=material_id)
    materiales = Material.objects.filter(id_solicitud=solicitud.id_solicitud)

    if request.method == 'GET':
        default_values = {'pendiente': False, 'compras': False, 'finanzas': False, 'sistemas': False,
                          'aprobado': False, 'rechazado_compras': False, 'rechazado_finanzas': False, 'rechazado_sistemas': False, 'eliminado': False}
        if request.user.compras:
            solicitud_form = SolicitudFormForCompras(
                instance=solicitud, initial=default_values)
        elif request.user.finanzas:
            solicitud_form = SolicitudFormForFinanzas(
                instance=solicitud, initial=default_values)
        elif request.user.sistemas:
            solicitud_form = SolicitudFormForSistemas(
                instance=solicitud, initial=default_values)
        else:
            solicitud_form = SolicitudDetailForm(
                instance=solicitud, initial=default_values)

        material_forms = [MaterialDetailForm(
            instance=material, prefix=f'material-{material.id}') for material in materiales]

        return render(request, 'material/material_detail.html', {
            'solicitud': solicitud,
            'solicitud_form': solicitud_form,
            'material_forms': material_forms,
            'current_user': request.user
        })
    else:
        try:
            if request.user.compras:
                solicitud_form = SolicitudFormForCompras(
                    request.POST, instance=solicitud)
            elif request.user.finanzas:
                solicitud_form = SolicitudFormForFinanzas(
                    request.POST, instance=solicitud)
            elif request.user.sistemas:
                solicitud_form = SolicitudFormForSistemas(
                    request.POST, instance=solicitud)
            else:
                solicitud_form = SolicitudForm(
                    request.POST, instance=solicitud)

            material_forms = [MaterialForm(
                request.POST, instance=material, prefix=f'material-{material.id}') for material in materiales]
            
            historial_form = HistorialForm(request.POST)

            if solicitud_form.is_valid() and all(form.is_valid() for form in material_forms) and historial_form.is_valid():
                solicitud_form.save()

                for form in material_forms:
                    form.save()
                
                # Guardar la modificación de la solicitud en el historial de cambios
                historial = historial_form.save(commit=False)
                historial.id_solicitud = solicitud.id
                if solicitud.rechazado_compras or solicitud.rechazado_finanzas or solicitud.rechazado_sistemas:
                    historial.accion = 'rechazada'
                elif solicitud.pendiente:
                    historial.accion = 'modificada'
                else:
                    historial.accion = 'aprobada'
                historial.usuario = request.user
                historial.save()

                return redirect('material')

        except ValueError:
            solicitud_form = SolicitudForm(instance=material)
            return render(request, 'material/material_detail.html', {
                'solicitud': solicitud,
                'form': solicitud_form,
                'error': 'Se produjo un error al actualizar, intente de nuevo'
            })
