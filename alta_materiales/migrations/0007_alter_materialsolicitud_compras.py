# Generated by Django 4.2.2 on 2023-08-31 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0006_materialsolicitud_comentarios_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialsolicitud',
            name='compras',
            field=models.BooleanField(default=False),
        ),
    ]
