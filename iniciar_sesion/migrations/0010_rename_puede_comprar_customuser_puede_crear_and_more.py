# Generated by Django 4.2.2 on 2023-10-04 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iniciar_sesion', '0009_alter_customuser_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='puede_comprar',
            new_name='puede_crear',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
