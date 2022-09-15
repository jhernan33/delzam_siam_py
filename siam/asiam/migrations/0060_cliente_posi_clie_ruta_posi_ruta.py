# Generated by Django 4.0.4 on 2022-09-02 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0059_ruta_nomb_ruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='posi_clie',
            field=models.IntegerField(blank=True, null=True, verbose_name='Posicion del Cliente para la Entrega'),
        ),
        migrations.AddField(
            model_name='ruta',
            name='posi_ruta',
            field=models.IntegerField(blank=True, null=True, verbose_name='Posicion de la Ruta'),
        ),
    ]
