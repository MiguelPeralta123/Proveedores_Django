# Generated by Django 4.2.2 on 2023-09-27 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0016_alter_proveedor_es_migracion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='razon_social',
        ),
    ]
