# Generated by Django 4.2 on 2023-10-25 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alta_proveedores', '0034_rename_monto_credito_proveedor_monto_credito_mn'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='monto_credito_me',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
    ]