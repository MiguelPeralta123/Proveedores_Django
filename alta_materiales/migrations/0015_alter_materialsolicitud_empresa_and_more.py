# Generated by Django 4.2.2 on 2023-09-26 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0014_remove_materialsolicitud_rfc_migracion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialsolicitud',
            name='empresa',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='materialsolicitud',
            name='justificacion',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]