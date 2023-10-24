from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.

class MaterialSolicitud(models.Model):
    id_solicitud = models.CharField(max_length=10)
    es_migracion = models.BooleanField(default=False)
    empresa_origen = models.CharField(max_length=50, blank=True)
    empresa_destino = models.CharField(max_length=50, blank=True)
    nombre_producto_migracion = models.CharField(max_length=50, blank=True)
    empresa = models.CharField(max_length=50, blank=True)
    justificacion = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comentarios = models.CharField(max_length=250, blank=True)
    pendiente = models.BooleanField(default=False)
    compras = models.BooleanField(default=False)
    finanzas = models.BooleanField(default=False)
    sistemas = models.BooleanField(default=False)
    aprobadas = models.BooleanField(default=False)
    rechazado_compras = models.BooleanField(default=False)
    rechazado_finanzas = models.BooleanField(default=False)
    rechazado_sistemas = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    borrador = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural = "solicitudes de materiales"

    def __str__(self):
        return str(self.id) + " - " + self.empresa + " - " + self.usuario.first_name + " " + self.usuario.last_name


class Material(models.Model):
    id_solicitud = models.CharField(max_length=10)
    tipo_alta = models.CharField(max_length=50, blank=True)
    subfamilia = models.CharField(max_length=50, blank=True)
    nombre_producto = models.CharField(max_length=50, blank=True)
    largo = models.CharField(max_length=20, blank=True)
    ancho = models.CharField(max_length=20, blank=True)
    alto = models.CharField(max_length=20, blank=True)
    calibre = models.CharField(max_length=20, blank=True)
    um_largo = models.CharField(max_length=20, blank=True)
    um_ancho = models.CharField(max_length=20, blank=True)
    um_alto = models.CharField(max_length=20, blank=True)
    um_calibre = models.CharField(max_length=20, blank=True)
    material = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=20, blank=True)
    marca = models.CharField(max_length=50, blank=True)
    parte_modelo = models.CharField(max_length=50, blank=True)
    nombre_comun = models.CharField(max_length=50, blank=True)
    es_mezcla = models.BooleanField(default=False)
    ing_activo = models.CharField(max_length=50, blank=True)
    porcentaje_iva = models.CharField(max_length=50, blank=True)
    alias = models.CharField(max_length=50, blank=True)
    unidad_medida = models.CharField(max_length=50, blank=True)
    codigo_sat = models.CharField(max_length=50, blank=True)
    es_material_empaque = models.BooleanField(default=False)
    es_prod_terminado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'material'
        verbose_name_plural = "materiales"

    def __str__(self):
        return str(self.id) + ".- " + self.tipo_alta + "/" + self.nombre_producto


class MaterialHistorial(models.Model):
    id_solicitud = models.IntegerField()
    accion = models.CharField(max_length=10)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'historial de solicitudes de material'
        verbose_name_plural = "historiales de solicitudes de material"

    def __str__(self):
        return "Solicitud " + self.accion + " por " + self.usuario.get_full_name()


# CATÁLOGOS
class CatalogoMaterial(models.Model):
    codigo = models.CharField(max_length=20)
    nombre_producto = models.CharField(max_length=150)
    subfamilia = models.CharField(max_length=100)
    familia = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Producto catálogo'
        verbose_name_plural = "Productos catálogo"

    def __str__(self):
        return self.codigo + " - " + self.nombre_producto