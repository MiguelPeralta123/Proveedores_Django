from django import forms
from django.forms import formset_factory
from .models import Material, MaterialSolicitud, MaterialHistorial
from .options import *

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
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

class SolicitudDetailForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'comentarios']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'})
        }

class SolicitudFormForCompras(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'comentarios']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control'})
        }

class SolicitudFormForFinanzas(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'comentarios']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control'})
        }

class SolicitudFormForSistemas(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'comentarios']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control'})
        }

class HistorialForm(forms.ModelForm):
    class Meta:
        model = MaterialHistorial
        fields = []