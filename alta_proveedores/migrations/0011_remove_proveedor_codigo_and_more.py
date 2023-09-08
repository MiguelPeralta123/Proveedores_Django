# Generated by Django 4.2.2 on 2023-09-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0010_proveedor_es_migracion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='dias_para_entrega_completa',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='impuesto_cedular',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='reg_inc_fiscal',
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='venc_s_fecha',
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='contacto',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='id_fiscal',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
