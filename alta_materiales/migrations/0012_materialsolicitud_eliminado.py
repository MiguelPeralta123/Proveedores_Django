# Generated by Django 4.2.2 on 2023-09-15 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0011_remove_material_familia_remove_material_tipo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialsolicitud',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
    ]
