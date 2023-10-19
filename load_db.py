import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proveedores.settings")
django.setup()

import csv
from alta_proveedores.models import CatalogoProveedor
from alta_materiales.models import CatalogoMaterial

def load_proveedores():
    with open('csv_files/catalogo_proveedores.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            CatalogoProveedor.objects.create(
                nombre=row[0],
                nombre_comercial=row[1],
                rfc=row[2],
            )

def load_materiales():
    with open('csv_files/catalogo_productos.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) # Skipping headers
        for row in csv_reader:
            CatalogoMaterial.objects.create(
                codigo=row[0],
                nombre_producto=row[1],
                subfamilia=row[2],
                familia=row[3],
            )

if __name__ == "__main__":
    load_proveedores()
    load_materiales()
