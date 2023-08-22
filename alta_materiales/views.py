from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import *
from .models import MaterialSolicitud, Material
# Decorator to protect routes from accessing before sign in
from django.contrib.auth.decorators import login_required

# Options lists
from .options import *

# Generando un id unico para cada solicitud
import random
import string

from django.forms import formset_factory

def generar_codigo_unico():
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(10))
    return codigo


# Create your views here.

# VISTAS DE MATERIAL (GET ALL, CREATE, DETAIL)

@login_required
def material(request):
    # Si el usuario tiene permisos de compras, podrá ver las solicitudes de todos los usuarios
    if request.user.compras:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por compras
        materiales = MaterialSolicitud.objects.filter(compras=False)
    elif request.user.finanzas:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por finanzas
        materiales = MaterialSolicitud.objects.filter(compras=True, finanzas=False)
    elif request.user.sistemas:
        # Trayendo de la base de datos todas las solicitudes que no hayan sido aprobadas por sistemas
        materiales = MaterialSolicitud.objects.filter(
            compras=True, finanzas=True, sistemas=False)
    else:
        # Trayendo de la base de datos los materiales que correspondan al usuario logueado
        materiales = MaterialSolicitud.objects.filter(usuario=request.user)

    return render(request, 'material/material.html', {
        'materiales': materiales
    })


def material_view(request):
    form_count = 1

    if request.method == 'POST':
        solicitud_form = SolicitudForm(request.POST)
        material_forms = [MaterialForm(request.POST, prefix=str(i)) for i in range(form_count)]

        if solicitud_form.is_valid() and all(form.is_valid() for form in material_forms):
            solicitud = solicitud_form.save()
            for form in material_forms:
                material = form.save(commit=False)
                material.solicitud = solicitud
                material.save()

            return redirect('material')
    else:
        solicitud_form = SolicitudForm()
        for i in range(form_count):
            material_forms = MaterialForm(prefix=str(i))

    return render(request, 'material/material_crear.html', {
        'solicitud_form': solicitud_form,
        'material_form': material_forms,
        'initial_form_count': form_count,
    })


#def material_view(request):
#    if request.method == 'POST':
#        solicitud_form = MaterialSolicitudForm(request.POST)
#        material_formset = MaterialFormset(request.POST, prefix='material')
#        
#        if solicitud_form.is_valid() and material_formset.is_valid():
#            # Process the main form data
#            #empresa = solicitud_form.cleaned_data['empresa']
#            #justificacion = solicitud_form.cleaned_data['justificacion']
#            print("Solicitud creada")
#            
#            # Process the nested formset data
#            for material_form in material_formset:
#                if material_form.is_valid():
#                    #nombre = material_form.cleaned_data['nombre']
#                    #tipo_alta = material_form.cleaned_data['tipo_alta']
#                    #tipo = material_form.cleaned_data['tipo']
#                    #familia = material_form.cleaned_data['familia']
#                    #subfamilia = material_form.cleaned_data['subfamilia']
#                    #unidad_medida = material_form.cleaned_data['unidad_medida']
#                    
#                    # Process the nested form data here or pass it to another view
#                    print("Material creado")
#            
#            # Redirect or render a success page
#            #return render(request, 'success.html')
#    else:
#        solicitud_form = MaterialSolicitudForm()
#        material_formset = MaterialFormset(prefix='material')
#    
#    return render(request, 'material/material_crear.html', {'solicitud_form': solicitud_form, 'material_formset': material_formset})


#def solicitud_material_view(request):
#    if request.method == 'POST':
#        material_solicitud_form = MaterialSolicitudForm(request.POST)
#        material_forms = [MaterialFormset(prefix=f'material-{i}', data=request.POST) for i in range(
#            1, len(request.POST) - 1) if f'material-{i}-nombre_producto' in request.POST]
#        
#        print(len(material_forms))
#
#        if material_solicitud_form.is_valid() and all(form.is_valid() for form in material_forms):
#            codigo = generar_codigo_unico()
#
#            form = material_solicitud_form
#            new_solicitud = form.save(commit=False)
#            new_solicitud.id_solicitud = codigo
#            new_solicitud.usuario = request.user
#            #new_solicitud.save()
#
#            for form in material_forms:
#                new_material = form.save(commit=False)
#                new_material.id_solicitud = codigo
#                #new_material.save()
#
#            #return redirect('material')
#    else:
#        material_solicitud_form = MaterialSolicitudForm()
#        material_forms = [MaterialForm(prefix='material-1')]
#
#    context = {
#        'material_solicitud_form': material_solicitud_form,
#        'material_forms': material_forms,
#        'tipo_list': TIPO_LIST,
#        'familia_list': FAMILIA_LIST,
#        'subfamilia_list': SUBFAMILIA_LIST,
#        'unidad_medida_list': UNIDAD_MEDIDA_LIST,
#    }
#    return render(request, 'material/solicitud_material.html', context)


@login_required
def material_detail(request, material_id):
    # Traemos el material que tenga el id que seleccionamos
    solicitud = get_object_or_404(MaterialSolicitud, pk=material_id)
    if request.method == 'GET':
        # Validamos si el usuario es compras para permitir aprobar solicitudes
        if request.user.compras:
            form = MaterialFormForCompras(instance=solicitud)
        else:
            # Validamos si el usuario es finanzas para permitir aprobar solicitudes
            if request.user.finanzas:
                form = MaterialFormForFinanzas(instance=solicitud)
            else:
                # Validamos si el usuario es sistemas para permitir aprobar solicitudes
                if request.user.sistemas:
                    form = MaterialFormForSistemas(instance=solicitud)
                else:
                    form = MaterialDetailForm(instance=solicitud)

        # Añadiendo un formulario por cada material de la solicitud
        materiales = Material.objects.filter(id_solicitud=solicitud.id_solicitud)
        MaterialFormSet = formset_factory(MaterialForm, extra=len(materiales))
        material_forms = MaterialFormSet(initial=[{'nombre_producto': material.nombre_producto, 'tipo_alta': material.tipo_alta, 'tipo': material.tipo, 'familia': material.familia, 'subfamilia': material.subfamilia, 'unidad_medida': material.unidad_medida} for material in materiales])

        print(materiales[1].unidad_medida)

        return render(request, 'material/material_detail.html', {
            'material': material,
            'form': form,
            'material_forms': material_forms
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
