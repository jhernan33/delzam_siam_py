# Generated by Django 4.0.4 on 2022-10-06 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0068_cliente_ruta_detalle_vendedor_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='ptor_clie',
            field=models.TextField(blank=True, null=True, verbose_name='Punto de Referencia del Cliente'),
        ),
    ]
