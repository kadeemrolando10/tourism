# Generated by Django 2.0.4 on 2018-08-03 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0014_auto_20180802_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretary',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='Nombre Completo'),
        ),
        migrations.AlterField(
            model_name='secretary',
            name='rol',
            field=models.CharField(max_length=100, verbose_name='Rol'),
        ),
    ]