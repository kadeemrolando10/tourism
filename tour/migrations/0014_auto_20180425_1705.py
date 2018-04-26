# Generated by Django 2.0.4 on 2018-04-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0013_auto_20180423_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourism_site',
            name='address',
            field=models.CharField(default='sn', max_length=150, verbose_name='Direccion'),
        ),
        migrations.AddField(
            model_name='tourism_site',
            name='schedule',
            field=models.CharField(default='--', max_length=150, verbose_name='Horarios'),
        ),
        migrations.AddField(
            model_name='tourism_site',
            name='web',
            field=models.CharField(default='nn', max_length=150, verbose_name='Pagina Web'),
        ),
    ]
