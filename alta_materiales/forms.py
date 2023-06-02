from django import forms
from .models import Material
from .options import *

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['empresa', 'nombre_producto', 'tipo_alta', 'tipo', 'familia', 'subfamilia', 'unidad_medida', 'justificacion']
        widgets = {
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_producto': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control', 'initial':''}),
            'familia': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control', 'initial':''}),
            'subfamilia': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control', 'initial':''}),
            'unidad_medida': forms.Select(choices=DEFAULT_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control'}),
        }


class MaterialDetailForm(forms.ModelForm):
    pass

class MaterialFormForCompras(forms.ModelForm):
    pass

class MaterialFormForFinanzas(forms.ModelForm):
    pass

class MaterialFormForSistemas(forms.ModelForm):
    pass