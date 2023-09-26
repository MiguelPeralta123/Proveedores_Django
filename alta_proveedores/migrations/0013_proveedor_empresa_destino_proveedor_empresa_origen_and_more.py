# Generated by Django 4.2.2 on 2023-09-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0012_proveedor_eliminado'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='empresa_destino',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='empresa_origen',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='rfc_migracion',
            field=models.CharField(blank=True, max_length=14),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='agente_aduanal',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='banco',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='calle',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='ciudad',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='clabe',
            field=models.CharField(blank=True, max_length=18),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='colonia',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='constancia_situacion_fiscal',
            field=models.FileField(blank=True, upload_to='static/documentos/constancias/'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='contribuyente',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='correo_general',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='correo_pagos',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='cuenta',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='dias_credito',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='empresa',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='estado',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='estado_cuenta_bancario',
            field=models.FileField(blank=True, upload_to='static/documentos/estados_cuenta'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='iva_frontera',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='limite_credito_ME',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='limite_credito_MN',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='localidad',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='moneda',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='monto_credito',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='municipio',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='nombre_comercial',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='nombre_fiscal',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='numero_exterior',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='pais',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='razon_social',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='regimen_capital',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='regimen_fiscal',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='retencion_isr',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='retencion_iva',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='rfc',
            field=models.CharField(blank=True, max_length=14),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='rubro',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono_1',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tipo_alta',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tipo_operacion',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tipo_tercero',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='uso_cfdi',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
