# Generated by Django 2.0.4 on 2018-07-12 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_auto_20180712_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourismroute',
            name='date',
            field=models.DateField(blank=True, verbose_name='Fecha de Evento'),
        ),
    ]
