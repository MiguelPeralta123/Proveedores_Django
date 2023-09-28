# Generated by Django 4.2.2 on 2023-09-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0010_materialsolicitud_es_migracion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='familia',
        ),
        migrations.RemoveField(
            model_name='material',
            name='tipo',
        ),
        migrations.AddField(
            model_name='material',
            name='alias',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='material',
            name='es_material_empaque',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='material',
            name='es_parte_original',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='material',
            name='es_prod_terminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='material',
            name='ing_activo',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='material',
            name='marca',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='material',
            name='medida',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='material',
            name='nombre_comun',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='material',
            name='parte_modelo',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='material',
            name='tipo_producto',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]