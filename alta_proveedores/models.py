from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.
class Proveedor(models.Model):
    es_migracion = models.BooleanField(default=False)
    empresa_origen = models.CharField(max_length=50, blank=True)
    empresa_destino = models.CharField(max_length=50, blank=True)
    rfc_migracion = models.CharField(max_length=14, blank=True)
    empresa = models.CharField(max_length=50, blank=True)
    tipo_alta = models.CharField(max_length=20, blank=True)
    contribuyente = models.CharField(max_length=20, blank=True)
    rfc = models.CharField(max_length=14, blank=True)
    curp = models.CharField(max_length=18, blank=True)
    regimen_capital = models.CharField(max_length=200, blank=True)
    nombre_fiscal = models.CharField(max_length=100, blank=True)
    nombre_comercial = models.CharField(max_length=100, blank=True)
    regimen_fiscal = models.CharField(max_length=100, blank=True)
    uso_cfdi = models.CharField(max_length=100, blank=True)
    representante_legal = models.CharField(max_length=50, blank=True)
    telefono_1 = models.CharField(max_length=10, blank=True)
    telefono_2 = models.CharField(max_length=10, blank=True)
    contacto = models.CharField(max_length=50, blank=True)
    correo_general = models.CharField(max_length=40, blank=True)
    correo_pagos = models.CharField(max_length=40, blank=True)
    sitio_web = models.CharField(max_length=30, blank=True)
    rubro = models.CharField(max_length=100, blank=True)
    tipo_operacion = models.CharField(max_length=10, blank=True)
    tipo_tercero = models.CharField(max_length=100, blank=True)
    id_fiscal = models.CharField(max_length=10, blank=True)
    agente_aduanal = models.CharField(max_length=10, blank=True)
    dias_credito = models.CharField(max_length=10, default=0, blank=True)
    limite_credito_MN = models.CharField(max_length=20, default=0, blank=True)
    limite_credito_ME = models.CharField(max_length=20, default=0, blank=True)
    monto_credito = models.CharField(max_length=20, default=0, blank=True)
    retencion_iva = models.CharField(max_length=10, blank=True)
    retencion_isr = models.CharField(max_length=10, blank=True)
    iva_frontera = models.CharField(max_length=10, blank=True)
    calle = models.CharField(max_length=50, blank=True)
    numero_exterior = models.CharField(max_length=10, blank=True)
    numero_interior = models.CharField(max_length=10, blank=True)
    codigo_postal = models.CharField(max_length=5, blank=True)
    colonia = models.CharField(max_length=50, blank=True)
    localidad = models.CharField(max_length=50, blank=True)
    municipio = models.CharField(max_length=30, blank=True)
    ciudad = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=20, blank=True)
    pais = models.CharField(max_length=20, blank=True)
    banco = models.CharField(max_length=50, blank=True)
    cuenta = models.CharField(max_length=20, blank=True)
    moneda = models.CharField(max_length=3, blank=True)
    clabe = models.CharField(max_length=18, blank=True)
    swift = models.CharField(max_length=20, blank=True)
    otro_codigo_bancario = models.CharField(max_length=20, blank=True)
    banco_2 = models.CharField(max_length=50, blank=True)
    cuenta_2 = models.CharField(max_length=20, blank=True)
    moneda_2 = models.CharField(max_length=3, blank=True)
    clabe_2 = models.CharField(max_length=18, blank=True)
    swift_2 = models.CharField(max_length=20, blank=True)
    otro_codigo_bancario_2 = models.CharField(max_length=20, blank=True)
    constancia_situacion_fiscal = models.FileField(upload_to='static/documentos/constancias', blank=True)
    estado_cuenta_bancario = models.FileField(upload_to='static/documentos/estados_cuenta', blank=True)
    pendiente = models.BooleanField(default=False)
    compras = models.BooleanField(default=False)
    finanzas = models.BooleanField(default=False)
    sistemas = models.BooleanField(default=False)
    aprobadas = models.BooleanField(default=False)
    rechazado_compras = models.BooleanField(default=False)
    rechazado_finanzas = models.BooleanField(default=False)
    rechazado_sistemas = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    usar_en_portal_proveedores = models.BooleanField(default=False)
    no_aplica_para_rafaga = models.BooleanField(default=False)
    no_relacionar_OC = models.BooleanField(default=False)
    comentarios = models.CharField(max_length=250, blank=True)
    borrador = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = "proveedores"

    def __str__(self):
        if self.rfc != '':
            return str(self.id) + ".- " + self.rfc + " - " + self.usuario.first_name + " " + self.usuario.last_name
        else:
            return str(self.id) + ".- Migración " + self.rfc_migracion + " - " + self.usuario.first_name + " " + self.usuario.last_name


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


# CATÁLOGOS
class CatalogoProveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_comercial = models.CharField(max_length=100)
    rfc = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Proveedor catálogo'
        verbose_name_plural = "Proveedores catálogo"

    def __str__(self):
        return self.rfc + " - " + self.nombre_comercial