# Generated by Django 4.2 on 2023-10-16 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0023_alter_proveedor_dias_credito_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='rubro',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tipo_tercero',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
