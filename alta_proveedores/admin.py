from django.contrib import admin
from .models import Proveedor

class ProveedorAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha',)

# Register your models here.
admin.site.register(Proveedor, ProveedorAdmin)