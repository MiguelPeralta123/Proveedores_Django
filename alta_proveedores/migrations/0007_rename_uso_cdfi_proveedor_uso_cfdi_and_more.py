# Generated by Django 4.2.2 on 2023-08-31 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0006_proveedor_comentarios'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proveedor',
            old_name='uso_cdfi',
            new_name='uso_cfdi',
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono_2',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
