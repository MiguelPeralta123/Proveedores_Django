# Generated by Django 4.2 on 2023-10-16 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0023_material_codigo_sat'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='um_alto',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='material',
            name='um_ancho',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='material',
            name='um_calibre',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='material',
            name='um_largo',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
