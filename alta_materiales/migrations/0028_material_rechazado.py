# Generated by Django 4.2 on 2023-10-26 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0027_material_ficha_tecnica_material_foto_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='rechazado',
            field=models.BooleanField(default=False),
        ),
    ]