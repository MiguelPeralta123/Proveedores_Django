# Generated by Django 4.2 on 2023-08-15 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0004_material_id_solicitud_materialsolicitud_id_solicitud_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'material', 'verbose_name_plural': 'materiales'},
        ),
        migrations.AlterModelOptions(
            name='materialsolicitud',
            options={'verbose_name': 'solicitud', 'verbose_name_plural': 'solicitudes de materiales'},
        ),
    ]