from django import forms
from django.forms import formset_factory
from .models import Material, MaterialSolicitud
from .options import *

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre_producto', 'tipo_alta', 'tipo', 'familia', 'subfamilia', 'unidad_medida']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class':'form-control material-nombre'}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control material-tipo-alta select-tipo-alta', 'initial':''}),
            'tipo': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-tipo select-tipo', 'initial':''}),
            'familia': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-familia select-familia', 'initial':''}),
            'subfamilia': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-subfamilia select-subfamilia', 'initial':''}),
            'unidad_medida': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control material-unidad-medida select-unidad-medida', 'initial':''}),
        }

class SolicitudMaterialDetailForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
        }

class MaterialDetailForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre_producto', 'tipo_alta', 'tipo', 'familia', 'subfamilia', 'unidad_medida']
        widgets = {
            # Make readonly: attrs={'class':'form-control material-nombre', 'readonly':'readonly'}
            'nombre_producto': forms.TextInput(attrs={'class':'form-control material-nombre'}),
            'tipo_alta': forms.TextInput(attrs={'class':'form-control material-tipo-alta'}),
            'tipo': forms.TextInput(attrs={'class':'form-control material-tipo'}),
            'familia': forms.TextInput(attrs={'class':'form-control material-familia'}),
            'subfamilia': forms.TextInput(attrs={'class':'form-control material-subfamilia'}),
            'unidad_medida': forms.TextInput(attrs={'class':'form-control material-unidad-medida'}),
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