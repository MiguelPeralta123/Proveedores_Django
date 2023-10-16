from django import forms
from django.forms import formset_factory
from .models import Material, MaterialSolicitud, MaterialHistorial
from .options import *

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'nombre_producto_migracion', 'empresa', 'justificacion', 'es_migracion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_producto_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_producto_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'eliminado': forms.HiddenInput(),
            'borrador': forms.HiddenInput(),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['tipo_alta', 'subfamilia', 'nombre_producto', 'largo', 'ancho', 'alto', 'calibre', 'material', 'color', 'marca', 'parte_modelo', 'nombre_comun', 'es_parte_original', 'ing_activo', 'tipo_producto', 'alias', 'unidad_medida', 'codigo_sat', 'es_material_empaque', 'es_prod_terminado']
        widgets = {
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control material-tipo-alta select-tipo-alta', 'initial':''}),
            'subfamilia': forms.Select(choices=SUBFAMILIA_LIST, attrs={'class':'form-control material-subfamilia select-subfamilia', 'initial':''}),
            'nombre_producto': forms.TextInput(attrs={'class':'form-control material-nombre'}),
            'largo': forms.TextInput(attrs={'class':'form-control material-largo'}),
            'ancho': forms.TextInput(attrs={'class':'form-control material-ancho'}),
            'alto': forms.TextInput(attrs={'class':'form-control material-alto'}),
            'calibre': forms.TextInput(attrs={'class':'form-control material-calibre'}),
            'material': forms.TextInput(attrs={'class':'form-control material-material'}),
            'color': forms.TextInput(attrs={'class':'form-control material-color'}),
            'marca': forms.TextInput(attrs={'class':'form-control material-marca'}),
            'parte_modelo': forms.TextInput(attrs={'class':'form-control material-parte-modelo'}),
            'nombre_comun': forms.TextInput(attrs={'class':'form-control material-nombre-comun'}),
            'es_parte_original': forms.CheckboxInput(attrs={'class':'form-checkbox material-es-parte-original'}),
            'ing_activo': forms.TextInput(attrs={'class':'form-control material-ing-activo'}),
            'tipo_producto': forms.TextInput(attrs={'class':'form-control material-tipo-producto'}),
            'alias': forms.TextInput(attrs={'class':'form-control material-alias'}),
            'unidad_medida': forms.Select(choices=UNIDAD_MEDIDA_LIST, attrs={'class':'form-control material-unidad-medida select-unidad-medida', 'initial':''}),
            'codigo_sat': forms.TextInput(attrs={'class':'form-control material-codigo-sat'}),
            'es_material_empaque': forms.CheckboxInput(attrs={'class':'form-checkbox material-es-material-empaque'}),
            'es_prod_terminado': forms.CheckboxInput(attrs={'class':'form-checkbox material-es-prod-terminado'}),
        }

class SolicitudDetailForm(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'nombre_producto_migracion', 'empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_producto_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'eliminado': forms.HiddenInput(),
            'borrador': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'})
        }

class MaterialDetailForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['tipo_alta', 'subfamilia', 'nombre_producto', 'largo', 'ancho', 'alto', 'calibre', 'material', 'color', 'marca', 'parte_modelo', 'nombre_comun', 'es_parte_original', 'ing_activo', 'tipo_producto', 'alias', 'unidad_medida', 'codigo_sat', 'es_material_empaque', 'es_prod_terminado']
        widgets = {
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control material-tipo-alta select-tipo-alta', 'initial':''}),
            'subfamilia': forms.Select(choices=SUBFAMILIA_LIST, attrs={'class':'form-control material-subfamilia select-subfamilia', 'initial':''}),
            'nombre_producto': forms.TextInput(attrs={'class':'form-control material-nombre'}),
            'largo': forms.TextInput(attrs={'class':'form-control material-largo'}),
            'ancho': forms.TextInput(attrs={'class':'form-control material-ancho'}),
            'alto': forms.TextInput(attrs={'class':'form-control material-alto'}),
            'calibre': forms.TextInput(attrs={'class':'form-control material-calibre'}),
            'material': forms.TextInput(attrs={'class':'form-control material-material'}),
            'color': forms.TextInput(attrs={'class':'form-control material-color'}),
            'marca': forms.TextInput(attrs={'class':'form-control material-marca'}),
            'parte_modelo': forms.TextInput(attrs={'class':'form-control material-parte-modelo'}),
            'nombre_comun': forms.TextInput(attrs={'class':'form-control material-nombre-comun'}),
            'es_parte_original': forms.CheckboxInput(attrs={'class':'form-checkbox material-es-parte-original'}),
            'ing_activo': forms.TextInput(attrs={'class':'form-control material-ing-activo'}),
            'tipo_producto': forms.TextInput(attrs={'class':'form-control material-tipo-producto'}),
            'alias': forms.TextInput(attrs={'class':'form-control material-alias'}),
            'unidad_medida': forms.Select(choices=UNIDAD_MEDIDA_LIST, attrs={'class':'form-control material-unidad-medida select-unidad-medida', 'initial':''}),
            'codigo_sat': forms.TextInput(attrs={'class':'form-control material-codigo-sat'}),
            'es_material_empaque': forms.CheckboxInput(attrs={'class':'form-checkbox material-es-material-empaque'}),
            'es_prod_terminado': forms.CheckboxInput(attrs={'class':'form-checkbox material-es-prod-terminado'}),
        }

class SolicitudFormForCompras(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'nombre_producto_migracion', 'empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_producto_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'eliminado': forms.HiddenInput(),
            'borrador': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control'})
        }

class SolicitudFormForFinanzas(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'nombre_producto_migracion', 'empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_producto_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'eliminado': forms.HiddenInput(),
            'borrador': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control'})
        }

class SolicitudFormForSistemas(forms.ModelForm):
    class Meta:
        model = MaterialSolicitud
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'nombre_producto_migracion', 'empresa', 'justificacion', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_producto_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'justificacion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'máximo 250 caracteres...'}),
            'pendiente': forms.HiddenInput(),
            'compras': forms.HiddenInput(),
            'finanzas': forms.HiddenInput(),
            'sistemas': forms.HiddenInput(),
            'rechazado_compras': forms.HiddenInput(),
            'rechazado_finanzas': forms.HiddenInput(),
            'rechazado_sistemas': forms.HiddenInput(),
            'eliminado': forms.HiddenInput(),
            'borrador': forms.HiddenInput(),
            'comentarios': forms.TextInput(attrs={'class':'form-control'})
        }

class HistorialForm(forms.ModelForm):
    class Meta:
        model = MaterialHistorial
        fields = []