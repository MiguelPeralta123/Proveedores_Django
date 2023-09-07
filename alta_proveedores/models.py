from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.
class Proveedor(models.Model):
    empresa = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10)
    tipo_alta = models.CharField(max_length=20)
    contribuyente = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=50)
    rfc = models.CharField(max_length=14)
    curp = models.CharField(max_length=18, blank=True)
    regimen_capital = models.CharField(max_length=100)
    nombre_fiscal = models.CharField(max_length=100)
    nombre_comercial = models.CharField(max_length=50)
    regimen_fiscal = models.CharField(max_length=100)
    uso_cfdi = models.CharField(max_length=100)
    representante_legal = models.CharField(max_length=50, blank=True)
    telefono_1 = models.CharField(max_length=10)
    telefono_2 = models.CharField(max_length=10, blank=True)
    contacto = models.CharField(max_length=50)
    grupo = models.CharField(max_length=50)
    correo_general = models.CharField(max_length=40)
    correo_pagos = models.CharField(max_length=40)
    sitio_web = models.CharField(max_length=30, blank=True)
    rubro = models.CharField(max_length=20)
    tipo_operacion = models.CharField(max_length=10)
    tipo_tercero = models.CharField(max_length=20)
    id_fiscal = models.CharField(max_length=10)
    regimen_fiscal = models.CharField(max_length=100)
    agente_aduanal = models.CharField(max_length=10)
    reg_inc_fiscal = models.CharField(max_length=10)
    impuesto_cedular = models.CharField(max_length=10)
    venc_s_fecha = models.DateField()
    dias_para_entrega_completa = models.PositiveIntegerField(default=0)
    dias_credito = models.PositiveIntegerField(default=0)
    limite_credito_MN = models.PositiveIntegerField(default=0)
    limite_credito_ME = models.PositiveIntegerField(default=0)
    monto_credito = models.PositiveIntegerField(default=0)
    retencion_iva = models.CharField(max_length=10)
    retencion_isr = models.CharField(max_length=10)
    iva_frontera = models.CharField(max_length=10)
    calle = models.CharField(max_length=50)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, blank=True)
    codigo_postal = models.CharField(max_length=5)
    colonia = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    municipio = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    pais = models.CharField(max_length=20)
    banco = models.CharField(max_length=50)
    cuenta = models.CharField(max_length=10)
    moneda = models.CharField(max_length=3)
    clabe = models.CharField(max_length=18)
    banco_2 = models.CharField(max_length=50, blank=True)
    cuenta_2 = models.CharField(max_length=10, blank=True)
    moneda_2 = models.CharField(max_length=3, blank=True)
    clabe_2 = models.CharField(max_length=18, blank=True)
    constancia_situacion_fiscal = models.FileField(upload_to='static/documentos/constancias/')
    estado_cuenta_bancario = models.FileField(upload_to='static/documentos/estados_cuenta')
    pendiente = models.BooleanField(default=False)
    compras = models.BooleanField(default=False)
    finanzas = models.BooleanField(default=False)
    sistemas = models.BooleanField(default=False)
    aprobadas = models.BooleanField(default=False)
    rechazado_compras = models.BooleanField(default=False)
    rechazado_finanzas = models.BooleanField(default=False)
    rechazado_sistemas = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    usar_en_portal_proveedores = models.BooleanField(default=False)
    no_aplica_para_rafaga = models.BooleanField(default=False)
    no_relacionar_OC = models.BooleanField(default=False)
    comentarios = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = "proveedores"

    def __str__(self):
        return str(self.id) + ".- " + self.razon_social + " - " + self.usuario.first_name + " " + self.usuario.last_name


class ProveedorHistorial(models.Model):
    id_proveedor = models.IntegerField()
    accion = models.CharField(max_length=10)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'historial de solicitudes de proveedor'
        verbose_name_plural = "historiales de solicitudes de proveedor"

    def __str__(self):
        return "Solicitud " + self.accion + " por " + self.usuario.get_full_name()
