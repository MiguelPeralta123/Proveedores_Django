# Generated by Django 4.2.2 on 2023-09-07 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0009_alter_materialhistorial_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialsolicitud',
            name='es_migracion',
            field=models.BooleanField(default=False),
        ),
    ]