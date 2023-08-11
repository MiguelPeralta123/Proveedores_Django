from django import forms
from django.forms import formset_factory
from .models import Material, MaterialSolicitud
from .options import *


class MaterialFormset(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre_producto', 'tipo_alta', 'tipo', 'familia', 'subfamilia', 'unidad_medida']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class':'form-control material-nombre'}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control material-tipo-alta', 'initial':''}),
            'tipo': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-tipo', 'initial':''}),
            'familia': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-familia', 'initial':''}),
            'subfamilia': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-subfamilia', 'initial':''}),
            'unidad_medida': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-unidad-medida', 'initial':''}),
        }


class MaterialSolicitudForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
        }
        NestedFormSet = formset_factory(MaterialFormset, extra=1)  # Set extra to control the number of forms displayed initially


class MaterialDetailForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
        }

class MaterialFormForCompras(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'compras']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
            'compras': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
        }

class MaterialFormForFinanzas(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'finanzas']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
            'finanzas': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
        }

class MaterialFormForSistemas(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'sistemas']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
            'sistemas': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
        }