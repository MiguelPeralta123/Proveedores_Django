# Generated by Django 4.2 on 2023-05-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(max_length=50)),
                ('nombre_producto', models.CharField(max_length=50)),
                ('tipo_alta', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
                ('familia', models.CharField(max_length=50)),
                ('subfamilia', models.CharField(max_length=50)),
                ('unidad_medida', models.CharField(max_length=50)),
                ('justificacion', models.CharField(max_length=255)),
                ('compras', models.BooleanField(default=False)),
                ('finanzas', models.BooleanField(default=False)),
                ('sistemas', models.BooleanField(default=False)),
                ('aprobadas', models.BooleanField(default=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
