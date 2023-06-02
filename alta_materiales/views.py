from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import MaterialForm, MaterialFormForCompras, MaterialFormForFinanzas, MaterialFormForSistemas, MaterialDetailForm
from .models import Material
# Decorator to protect routes from accessing before sign in
from django.contrib.auth.decorators import login_required

# Options lists
from .options import *

# Create your views here.

# VISTAS DE PROVEEDOR (GET ALL, CREATE, DETAIL)


@login_required
def material(request):
    # Si el usuario tiene permisos de compras, podrá ver las solicitudes de todos los usuarios
    if request.user.compras:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por compras
        materiales = Material.objects.filter(compras=False)
    elif request.user.finanzas:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por finanzas
        materiales = Material.objects.filter(compras=True, finanzas=False)
    elif request.user.sistemas:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por sistemas
        materiales = Material.objects.filter(
            compras=True, finanzas=True, sistemas=False)
    else:
        # Trayendo de la base de datos los materiales que correspondan al usuario logueado
        materiales = Material.objects.filter(usuario=request.user)

    return render(request, 'material/material.html', {
        'materiales': materiales
    })


@login_required
def material_create(request):
    # Verificamos si el usuario tiene permisos para requerir, en caso contrario, lo redireccionamos a la ventana de materiales
    if request.user.puede_comprar:
        if request.method == 'GET':
            return render(request, 'material/material_create.html', {
                'form': MaterialForm,
                'tipo_list': TIPO_LIST,
                'familia_list': FAMILIA_LIST,
                'subfamilia_list': SUBFAMILIA_LIST,
                'unidad_medida_list': UNIDAD_MEDIDA_LIST,
            })
        else:
            try:
                form = MaterialForm(request.POST)
                new_material = form.save(commit=False)
                new_material.usuario = request.user
                new_material.save()
                return redirect('material')
            except ValueError:
                return render(request, 'material/material_create.html', {
                    'form': MaterialForm,
                    'error': 'Por favor ingrese datos válidos'
                })
    else:
        return redirect('material')


@login_required
def material_detail(request, material_id):
    # Traemos el material que tenga el id que seleccionamos
    material = get_object_or_404(Material, pk=material_id)
    if request.method == 'GET':
        # Validamos si el usuario es compras para permitir aprobar solicitudes
        if request.user.compras:
            form = MaterialFormForCompras(instance=material)
        else:
            # Validamos si el usuario es finanzas para permitir aprobar solicitudes
            if request.user.finanzas:
                form = MaterialFormForFinanzas(instance=material)
            else:
                # Validamos si el usuario es sistemas para permitir aprobar solicitudes
                if request.user.sistemas:
                    form = MaterialFormForSistemas(instance=material)
                else:
                    form = MaterialDetailForm(instance=material)
        return render(request, 'material/material_detail.html', {
            'material': material,
            'form': form
        })
    else:
        try:
            # Validamos si el usuario es compras para permitir aprobar solicitudes
            if request.user.compras:
                form = MaterialFormForCompras(request.POST, instance=material)
            else:
                # Validamos si el usuario es finanzas para permitir aprobar solicitudes
                if request.user.finanzas:
                    form = MaterialFormForFinanzas(
                        request.POST, instance=material)
                else:
                    # Validamos si el usuario es sistemas para permitir aprobar solicitudes
                    if request.user.sistemas:
                        form = MaterialFormForSistemas(
                            request.POST, instance=material)
                    else:
                        form = MaterialDetailForm(
                            request.POST, instance=material)
            form.save()
            return redirect('material')
        except ValueError:
            form = MaterialDetailForm(instance=material)
            return render(request, 'material/material_detail.html', {
                'material': material,
                'form': form,
                'error': 'Se produjo un error al actualizar, intente de nuevo'
            })
