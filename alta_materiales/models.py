from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.
class MaterialSolicitud(models.Model):
    id_solicitud = models.CharField(max_length=10, default='123')
    empresa = models.CharField(max_length=50)
    justificacion = models.CharField(max_length=255)
    compras = models.BooleanField(default=True)
    finanzas = models.BooleanField(default=False)
    sistemas = models.BooleanField(default=False)
    aprobadas = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural = "solicitudes de materiales"

    def __str__(self):
        return str(self.id) + " - " + self.empresa + " - " + self.usuario.first_name + " " + self.usuario.last_name

class Material(models.Model):
    id_solicitud = models.CharField(max_length=10, default='123')
    nombre_producto = models.CharField(max_length=50)
    tipo_alta = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    familia = models.CharField(max_length=50)
    subfamilia = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'material'
        verbose_name_plural = "materiales"

    def __str__(self):
        return str(self.id) + ".- " + self.tipo + "/" + self.nombre_producto