# Generated by Django 4.2.2 on 2023-09-06 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0007_rename_uso_cdfi_proveedor_uso_cfdi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='rfc',
            field=models.CharField(max_length=14),
        ),
    ]
