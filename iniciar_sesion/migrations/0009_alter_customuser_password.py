# Generated by Django 4.2.2 on 2023-10-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iniciar_sesion', '0008_alter_customuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
