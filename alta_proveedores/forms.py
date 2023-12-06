from django import forms
import re
from .models import Proveedor, ProveedorHistorial
from datetime import date
from django.db.models import Q
from iniciar_sesion.models import CustomUser
from .options import *

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'rfc_migracion', 'empresa', 'tipo_alta', 'contribuyente', 'rfc', 'curp', 'regimen_capital', 'nombre_fiscal', 'nombre_comercial', 'regimen_fiscal', 'uso_cfdi', 'representante_legal', 'telefono_1', 'telefono_2', 'contacto', 'correo_general', 'correo_pagos', 'sitio_web', 'rubro', 'tipo_operacion', 'tipo_tercero', 'id_fiscal', 'agente_aduanal', 'fair_trade', 'dias_credito', 'monto_credito_mn', 'monto_credito_me', 'retencion_iva', 'retencion_isr', 'iva_frontera', 'codigo_postal', 'pais', 'estado', 'ciudad', 'municipio', 'localidad', 'colonia', 'calle', 'numero_exterior', 'numero_interior', 'banco', 'cuenta', 'moneda', 'clabe', 'swift', 'otro_codigo_bancario', 'banco_2', 'cuenta_2', 'moneda_2', 'clabe_2', 'swift_2', 'otro_codigo_bancario_2', 'usar_en_portal_proveedores', 'no_aplica_para_rafaga', 'no_relacionar_OC', 'constancia_situacion_fiscal', 'estado_cuenta_bancario', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_ORIGEN_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_DESTINO_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control', 'initial':''}),
            'contribuyente': forms.Select(choices=CONTRIBUYENTE_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc': forms.TextInput(attrs={'class':'form-control'}),
            'curp': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_capital': forms.Select(choices=REGIMEN_CAPITAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_fiscal': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_fiscal': forms.Select(choices=REGIMEN_FISCAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'uso_cfdi': forms.Select(choices=USO_CFDI_LIST, attrs={'class':'form-control', 'initial':''}),
            'representante_legal': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_1': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_2': forms.TextInput(attrs={'class':'form-control'}),
            'contacto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre de la persona'}),
            'correo_general': forms.TextInput(attrs={'class':'form-control'}),
            'correo_pagos': forms.TextInput(attrs={'class':'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class':'form-control'}),
            'rubro': forms.Select(choices=RUBRO_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_operacion': forms.Select(choices=TIPO_OPERACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_tercero': forms.Select(choices=TIPO_TERCERO_LIST, attrs={'class':'form-control', 'initial':''}),
            'id_fiscal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'para proveedores extranjeros'}),
            'agente_aduanal': forms.Select(choices=AGENTE_ADUANAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'fair_trade': forms.TextInput(attrs={'class':'form-control'}),
            'dias_credito': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_mn': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_me': forms.TextInput(attrs={'class':'form-control'}),
            'retencion_iva': forms.Select(choices=RETENCION_IVA_LIST, attrs={'class':'form-control', 'initial':''}),
            'retencion_isr': forms.Select(choices=RETENCION_ISR_LIST, attrs={'class':'form-control', 'initial':''}),
            'iva_frontera': forms.Select(choices=IVA_FRONTERA_LIST, attrs={'class':'form-control', 'initial':''}),
            'codigo_postal': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control'}),
            'municipio': forms.TextInput(attrs={'class':'form-control'}),
            'localidad': forms.TextInput(attrs={'class':'form-control'}),
            'colonia': forms.TextInput(attrs={'class':'form-control'}),
            'calle': forms.TextInput(attrs={'class':'form-control'}),
            'numero_exterior': forms.TextInput(attrs={'class':'form-control'}),
            'numero_interior': forms.TextInput(attrs={'class':'form-control'}),
            'banco': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe': forms.TextInput(attrs={'class':'form-control'}),
            'swift': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario': forms.TextInput(attrs={'class':'form-control'}),
            'banco_2': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta_2': forms.TextInput(attrs={'class':'form-control'}),
            'moneda_2': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe_2': forms.TextInput(attrs={'class':'form-control'}),
            'swift_2': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario_2': forms.TextInput(attrs={'class':'form-control'}),
            'usar_en_portal_proveedores': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_aplica_para_rafaga': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_relacionar_OC': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'constancia_situacion_fiscal': forms.FileInput(attrs={'class':'form-file'}),
            'estado_cuenta_bancario': forms.FileInput(attrs={'class':'form-file'}),
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

class ProveedorDetailForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'rfc_migracion', 'empresa', 'tipo_alta', 'contribuyente', 'rfc', 'curp', 'regimen_capital', 'nombre_fiscal', 'nombre_comercial', 'regimen_fiscal', 'uso_cfdi', 'representante_legal', 'telefono_1', 'telefono_2', 'contacto', 'correo_general', 'correo_pagos', 'sitio_web', 'rubro', 'tipo_operacion', 'tipo_tercero', 'id_fiscal', 'agente_aduanal', 'fair_trade', 'dias_credito', 'monto_credito_mn', 'monto_credito_me', 'retencion_iva', 'retencion_isr', 'iva_frontera', 'codigo_postal', 'pais', 'estado', 'ciudad', 'municipio', 'localidad', 'colonia', 'calle', 'numero_exterior', 'numero_interior', 'banco', 'cuenta', 'moneda', 'clabe', 'swift', 'otro_codigo_bancario', 'banco_2', 'cuenta_2', 'moneda_2', 'clabe_2', 'swift_2', 'otro_codigo_bancario_2', 'usar_en_portal_proveedores', 'no_aplica_para_rafaga', 'no_relacionar_OC', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_ORIGEN_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_DESTINO_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control', 'initial':''}),
            'contribuyente': forms.Select(choices=CONTRIBUYENTE_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc': forms.TextInput(attrs={'class':'form-control'}),
            'curp': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_capital': forms.Select(choices=REGIMEN_CAPITAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_fiscal': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_fiscal': forms.Select(choices=REGIMEN_FISCAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'uso_cfdi': forms.Select(choices=USO_CFDI_LIST, attrs={'class':'form-control', 'initial':''}),
            'representante_legal': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_1': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_2': forms.TextInput(attrs={'class':'form-control'}),
            'contacto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre de la persona'}),
            'correo_general': forms.TextInput(attrs={'class':'form-control'}),
            'correo_pagos': forms.TextInput(attrs={'class':'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class':'form-control'}),
            'rubro': forms.Select(choices=RUBRO_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_operacion': forms.Select(choices=TIPO_OPERACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_tercero': forms.Select(choices=TIPO_TERCERO_LIST, attrs={'class':'form-control', 'initial':''}),
            'id_fiscal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'para proveedores extranjeros'}),
            'agente_aduanal': forms.Select(choices=AGENTE_ADUANAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'fair_trade': forms.TextInput(attrs={'class':'form-control'}),
            'dias_credito': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_mn': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_me': forms.TextInput(attrs={'class':'form-control'}),
            'retencion_iva': forms.Select(choices=RETENCION_IVA_LIST, attrs={'class':'form-control', 'initial':''}),
            'retencion_isr': forms.Select(choices=RETENCION_ISR_LIST, attrs={'class':'form-control', 'initial':''}),
            'iva_frontera': forms.Select(choices=IVA_FRONTERA_LIST, attrs={'class':'form-control', 'initial':''}),
            'codigo_postal': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control'}),
            'municipio': forms.TextInput(attrs={'class':'form-control'}),
            'localidad': forms.TextInput(attrs={'class':'form-control'}),
            'colonia': forms.TextInput(attrs={'class':'form-control'}),
            'calle': forms.TextInput(attrs={'class':'form-control'}),
            'numero_exterior': forms.TextInput(attrs={'class':'form-control'}),
            'numero_interior': forms.TextInput(attrs={'class':'form-control'}),
            'banco': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe': forms.TextInput(attrs={'class':'form-control'}),
            'swift': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario': forms.TextInput(attrs={'class':'form-control'}),
            'banco_2': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta_2': forms.TextInput(attrs={'class':'form-control'}),
            'moneda_2': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe_2': forms.TextInput(attrs={'class':'form-control'}),
            'swift_2': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario_2': forms.TextInput(attrs={'class':'form-control'}),
            'usar_en_portal_proveedores': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_aplica_para_rafaga': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_relacionar_OC': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
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

class ProveedorFormForCompras(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'rfc_migracion', 'empresa', 'tipo_alta', 'contribuyente', 'rfc', 'curp', 'regimen_capital', 'nombre_fiscal', 'nombre_comercial', 'regimen_fiscal', 'uso_cfdi', 'representante_legal', 'telefono_1', 'telefono_2', 'contacto', 'correo_general', 'correo_pagos', 'sitio_web', 'rubro', 'tipo_operacion', 'tipo_tercero', 'id_fiscal', 'agente_aduanal', 'fair_trade', 'dias_credito', 'monto_credito_mn', 'monto_credito_me', 'retencion_iva', 'retencion_isr', 'iva_frontera', 'codigo_postal', 'pais', 'estado', 'ciudad', 'municipio', 'localidad', 'colonia', 'calle', 'numero_exterior', 'numero_interior', 'banco', 'cuenta', 'moneda', 'clabe', 'swift', 'otro_codigo_bancario', 'banco_2', 'cuenta_2', 'moneda_2', 'clabe_2', 'swift_2', 'otro_codigo_bancario_2', 'usar_en_portal_proveedores', 'no_aplica_para_rafaga', 'no_relacionar_OC', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_ORIGEN_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_DESTINO_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control', 'initial':''}),
            'contribuyente': forms.Select(choices=CONTRIBUYENTE_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc': forms.TextInput(attrs={'class':'form-control'}),
            'curp': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_capital': forms.Select(choices=REGIMEN_CAPITAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_fiscal': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_fiscal': forms.Select(choices=REGIMEN_FISCAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'uso_cfdi': forms.Select(choices=USO_CFDI_LIST, attrs={'class':'form-control', 'initial':''}),
            'representante_legal': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_1': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_2': forms.TextInput(attrs={'class':'form-control'}),
            'contacto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre de la persona'}),
            'correo_general': forms.TextInput(attrs={'class':'form-control'}),
            'correo_pagos': forms.TextInput(attrs={'class':'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class':'form-control'}),
            'rubro': forms.Select(choices=RUBRO_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_operacion': forms.Select(choices=TIPO_OPERACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_tercero': forms.Select(choices=TIPO_TERCERO_LIST, attrs={'class':'form-control', 'initial':''}),
            'id_fiscal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'para proveedores extranjeros'}),
            'agente_aduanal': forms.Select(choices=AGENTE_ADUANAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'fair_trade': forms.TextInput(attrs={'class':'form-control'}),
            'dias_credito': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_mn': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_me': forms.TextInput(attrs={'class':'form-control'}),
            'retencion_iva': forms.Select(choices=RETENCION_IVA_LIST, attrs={'class':'form-control', 'initial':''}),
            'retencion_isr': forms.Select(choices=RETENCION_ISR_LIST, attrs={'class':'form-control', 'initial':''}),
            'iva_frontera': forms.Select(choices=IVA_FRONTERA_LIST, attrs={'class':'form-control', 'initial':''}),
            'codigo_postal': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control'}),
            'municipio': forms.TextInput(attrs={'class':'form-control'}),
            'localidad': forms.TextInput(attrs={'class':'form-control'}),
            'colonia': forms.TextInput(attrs={'class':'form-control'}),
            'calle': forms.TextInput(attrs={'class':'form-control'}),
            'numero_exterior': forms.TextInput(attrs={'class':'form-control'}),
            'numero_interior': forms.TextInput(attrs={'class':'form-control'}),
            'banco': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe': forms.TextInput(attrs={'class':'form-control'}),
            'swift': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario': forms.TextInput(attrs={'class':'form-control'}),
            'banco_2': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta_2': forms.TextInput(attrs={'class':'form-control'}),
            'moneda_2': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe_2': forms.TextInput(attrs={'class':'form-control'}),
            'swift_2': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario_2': forms.TextInput(attrs={'class':'form-control'}),
            'usar_en_portal_proveedores': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_aplica_para_rafaga': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_relacionar_OC': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
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

class ProveedorFormForFinanzas(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'rfc_migracion', 'empresa', 'tipo_alta', 'contribuyente', 'rfc', 'curp', 'regimen_capital', 'nombre_fiscal', 'nombre_comercial', 'regimen_fiscal', 'uso_cfdi', 'representante_legal', 'telefono_1', 'telefono_2', 'contacto', 'correo_general', 'correo_pagos', 'sitio_web', 'rubro', 'tipo_operacion', 'tipo_tercero', 'id_fiscal', 'agente_aduanal', 'fair_trade', 'dias_credito', 'monto_credito_mn', 'monto_credito_me', 'retencion_iva', 'retencion_isr', 'iva_frontera', 'codigo_postal', 'pais', 'estado', 'ciudad', 'municipio', 'localidad', 'colonia', 'calle', 'numero_exterior', 'numero_interior', 'banco', 'cuenta', 'moneda', 'clabe', 'swift', 'otro_codigo_bancario', 'banco_2', 'cuenta_2', 'moneda_2', 'clabe_2', 'swift_2', 'otro_codigo_bancario_2', 'usar_en_portal_proveedores', 'no_aplica_para_rafaga', 'no_relacionar_OC', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_ORIGEN_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_DESTINO_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control', 'initial':''}),
            'contribuyente': forms.Select(choices=CONTRIBUYENTE_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc': forms.TextInput(attrs={'class':'form-control'}),
            'curp': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_capital': forms.Select(choices=REGIMEN_CAPITAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_fiscal': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_fiscal': forms.Select(choices=REGIMEN_FISCAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'uso_cfdi': forms.Select(choices=USO_CFDI_LIST, attrs={'class':'form-control', 'initial':''}),
            'representante_legal': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_1': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_2': forms.TextInput(attrs={'class':'form-control'}),
            'contacto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre de la persona'}),
            'correo_general': forms.TextInput(attrs={'class':'form-control'}),
            'correo_pagos': forms.TextInput(attrs={'class':'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class':'form-control'}),
            'rubro': forms.Select(choices=RUBRO_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_operacion': forms.Select(choices=TIPO_OPERACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_tercero': forms.Select(choices=TIPO_TERCERO_LIST, attrs={'class':'form-control', 'initial':''}),
            'id_fiscal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'para proveedores extranjeros'}),
            'agente_aduanal': forms.Select(choices=AGENTE_ADUANAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'fair_trade': forms.TextInput(attrs={'class':'form-control'}),
            'dias_credito': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_mn': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_me': forms.TextInput(attrs={'class':'form-control'}),
            'retencion_iva': forms.Select(choices=RETENCION_IVA_LIST, attrs={'class':'form-control', 'initial':''}),
            'retencion_isr': forms.Select(choices=RETENCION_ISR_LIST, attrs={'class':'form-control', 'initial':''}),
            'iva_frontera': forms.Select(choices=IVA_FRONTERA_LIST, attrs={'class':'form-control', 'initial':''}),
            'codigo_postal': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control'}),
            'municipio': forms.TextInput(attrs={'class':'form-control'}),
            'localidad': forms.TextInput(attrs={'class':'form-control'}),
            'colonia': forms.TextInput(attrs={'class':'form-control'}),
            'calle': forms.TextInput(attrs={'class':'form-control'}),
            'numero_exterior': forms.TextInput(attrs={'class':'form-control'}),
            'numero_interior': forms.TextInput(attrs={'class':'form-control'}),
            'banco': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe': forms.TextInput(attrs={'class':'form-control'}),
            'swift': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario': forms.TextInput(attrs={'class':'form-control'}),
            'banco_2': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta_2': forms.TextInput(attrs={'class':'form-control'}),
            'moneda_2': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe_2': forms.TextInput(attrs={'class':'form-control'}),
            'swift_2': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario_2': forms.TextInput(attrs={'class':'form-control'}),
            'usar_en_portal_proveedores': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_aplica_para_rafaga': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_relacionar_OC': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
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

class ProveedorFormForSistemas(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['es_migracion', 'empresa_origen', 'empresa_destino', 'rfc_migracion', 'empresa', 'tipo_alta', 'contribuyente', 'rfc', 'curp', 'regimen_capital', 'nombre_fiscal', 'nombre_comercial', 'regimen_fiscal', 'uso_cfdi', 'representante_legal', 'telefono_1', 'telefono_2', 'contacto', 'correo_general', 'correo_pagos', 'sitio_web', 'rubro', 'tipo_operacion', 'tipo_tercero', 'id_fiscal', 'agente_aduanal', 'fair_trade', 'dias_credito', 'monto_credito_mn', 'monto_credito_me', 'retencion_iva', 'retencion_isr', 'iva_frontera', 'codigo_postal', 'pais', 'estado', 'ciudad', 'municipio', 'localidad', 'colonia', 'calle', 'numero_exterior', 'numero_interior', 'banco', 'cuenta', 'moneda', 'clabe', 'swift', 'otro_codigo_bancario', 'banco_2', 'cuenta_2', 'moneda_2', 'clabe_2', 'swift_2', 'otro_codigo_bancario_2', 'usar_en_portal_proveedores', 'no_aplica_para_rafaga', 'no_relacionar_OC', 'pendiente', 'compras', 'finanzas', 'sistemas', 'rechazado_compras', 'rechazado_finanzas', 'rechazado_sistemas', 'eliminado', 'borrador', 'comentarios']
        widgets = {
            'es_migracion': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'empresa_origen': forms.Select(choices=EMPRESA_MIGRACION_ORIGEN_LIST, attrs={'class':'form-control', 'initial':''}),
            'empresa_destino': forms.Select(choices=EMPRESA_MIGRACION_DESTINO_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc_migracion': forms.TextInput(attrs={'class':'form-control'}),
            'empresa': forms.Select(choices=EMPRESA_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_alta': forms.Select(choices=TIPO_ALTA_LIST, attrs={'class':'form-control', 'initial':''}),
            'contribuyente': forms.Select(choices=CONTRIBUYENTE_LIST, attrs={'class':'form-control', 'initial':''}),
            'rfc': forms.TextInput(attrs={'class':'form-control'}),
            'curp': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_capital': forms.Select(choices=REGIMEN_CAPITAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'nombre_fiscal': forms.TextInput(attrs={'class':'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class':'form-control'}),
            'regimen_fiscal': forms.Select(choices=REGIMEN_FISCAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'uso_cfdi': forms.Select(choices=USO_CFDI_LIST, attrs={'class':'form-control', 'initial':''}),
            'representante_legal': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_1': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_2': forms.TextInput(attrs={'class':'form-control'}),
            'contacto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre de la persona'}),
            'correo_general': forms.TextInput(attrs={'class':'form-control'}),
            'correo_pagos': forms.TextInput(attrs={'class':'form-control'}),
            'sitio_web': forms.TextInput(attrs={'class':'form-control'}),
            'rubro': forms.Select(choices=RUBRO_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_operacion': forms.Select(choices=TIPO_OPERACION_LIST, attrs={'class':'form-control', 'initial':''}),
            'tipo_tercero': forms.Select(choices=TIPO_TERCERO_LIST, attrs={'class':'form-control', 'initial':''}),
            'id_fiscal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'para proveedores extranjeros'}),
            'agente_aduanal': forms.Select(choices=AGENTE_ADUANAL_LIST, attrs={'class':'form-control', 'initial':''}),
            'fair_trade': forms.TextInput(attrs={'class':'form-control'}),
            'dias_credito': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_mn': forms.TextInput(attrs={'class':'form-control'}),
            'monto_credito_me': forms.TextInput(attrs={'class':'form-control'}),
            'retencion_iva': forms.Select(choices=RETENCION_IVA_LIST, attrs={'class':'form-control', 'initial':''}),
            'retencion_isr': forms.Select(choices=RETENCION_ISR_LIST, attrs={'class':'form-control', 'initial':''}),
            'iva_frontera': forms.Select(choices=IVA_FRONTERA_LIST, attrs={'class':'form-control', 'initial':''}),
            'codigo_postal': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control'}),
            'municipio': forms.TextInput(attrs={'class':'form-control'}),
            'localidad': forms.TextInput(attrs={'class':'form-control'}),
            'colonia': forms.TextInput(attrs={'class':'form-control'}),
            'calle': forms.TextInput(attrs={'class':'form-control'}),
            'numero_exterior': forms.TextInput(attrs={'class':'form-control'}),
            'numero_interior': forms.TextInput(attrs={'class':'form-control'}),
            'banco': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe': forms.TextInput(attrs={'class':'form-control'}),
            'swift': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario': forms.TextInput(attrs={'class':'form-control'}),
            'banco_2': forms.Select(choices=BANCO_LIST, attrs={'class':'form-control', 'initial':''}),
            'cuenta_2': forms.TextInput(attrs={'class':'form-control'}),
            'moneda_2': forms.Select(choices=MONEDA_LIST, attrs={'class':'form-control', 'initial':''}),
            'clabe_2': forms.TextInput(attrs={'class':'form-control'}),
            'swift_2': forms.TextInput(attrs={'class':'form-control'}),
            'otro_codigo_bancario_2': forms.TextInput(attrs={'class':'form-control'}),
            'usar_en_portal_proveedores': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_aplica_para_rafaga': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
            'no_relacionar_OC': forms.CheckboxInput(attrs={'class':'form-checkbox'}),
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
        model = ProveedorHistorial
        fields = []