# Generated by Django 4.2 on 2023-08-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0003_alter_proveedor_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='rechazado_compras',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='rechazado_finanzas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='rechazado_sistemas',
            field=models.BooleanField(default=False),
        ),
    ]
