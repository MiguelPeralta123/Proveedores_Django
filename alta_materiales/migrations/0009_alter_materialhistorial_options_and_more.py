# Generated by Django 4.2.2 on 2023-09-06 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_materiales', '0008_materialhistorial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materialhistorial',
            options={'verbose_name': 'historial de solicitudes de material', 'verbose_name_plural': 'historiales de solicitudes de material'},
        ),
        migrations.AlterField(
            model_name='materialhistorial',
            name='id_solicitud',
            field=models.IntegerField(),
        ),
    ]
