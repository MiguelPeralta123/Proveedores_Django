# Generated by Django 4.2.2 on 2023-09-06 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alta_materiales', '0007_alter_materialsolicitud_compras'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_solicitud', models.CharField(max_length=10)),
                ('accion', models.CharField(max_length=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'solicitud',
                'verbose_name_plural': 'solicitudes de materiales',
            },
        ),
    ]
