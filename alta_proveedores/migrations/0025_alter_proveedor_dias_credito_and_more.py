# Generated by Django 4.2 on 2023-10-17 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0024_alter_proveedor_rubro_alter_proveedor_tipo_tercero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='dias_credito',
            field=models.CharField(blank=True, default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='limite_credito_ME',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='limite_credito_MN',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='monto_credito',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
    ]