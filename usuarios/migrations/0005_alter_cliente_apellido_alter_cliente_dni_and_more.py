# Generated by Django 4.1.7 on 2023-05-05 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_auto_20230430_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='apellido',
            field=models.CharField(max_length=20, verbose_name='Apellido'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.PositiveIntegerField(unique=True, verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=20, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.PositiveIntegerField(max_length=12, verbose_name='Telefono'),
        ),
    ]
