# Generated by Django 4.2.2 on 2023-09-26 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0013_materialsolicitud_empresa_destino_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialsolicitud',
            name='rfc_migracion',
        ),
        migrations.AddField(
            model_name='materialsolicitud',
            name='nombre_producto_migracion',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
