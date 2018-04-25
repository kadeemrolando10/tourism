# Generated by Django 2.0.4 on 2018-04-23 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0012_auto_20180423_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.1, max_digits=2, verbose_name='Calificacion'),
        ),
        migrations.AddField(
            model_name='lodgment',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.1, max_digits=2, verbose_name='Calificacion'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.1, max_digits=2, verbose_name='Calificacion'),
        ),
        migrations.AddField(
            model_name='tourism_site',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.1, max_digits=2, verbose_name='Calificacion'),
        ),
        migrations.AddField(
            model_name='transport',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.1, max_digits=2, verbose_name='Calificacion'),
        ),
    ]