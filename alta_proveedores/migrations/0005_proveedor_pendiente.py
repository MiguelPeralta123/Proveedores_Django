# Generated by Django 4.2 on 2023-08-16 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0004_proveedor_rechazado_compras_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='pendiente',
            field=models.BooleanField(default=False),
        ),
    ]