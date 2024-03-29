# Generated by Django 4.2.2 on 2023-08-24 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0005_alter_material_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialsolicitud',
            name='comentarios',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='materialsolicitud',
            name='pendiente',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='materialsolicitud',
            name='rechazado_compras',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='materialsolicitud',
            name='rechazado_finanzas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='materialsolicitud',
            name='rechazado_sistemas',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='material',
            name='id_solicitud',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='materialsolicitud',
            name='id_solicitud',
            field=models.CharField(max_length=10),
        ),
    ]
