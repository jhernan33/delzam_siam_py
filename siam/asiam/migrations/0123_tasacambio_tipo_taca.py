# Generated by Django 4.1.3 on 2024-02-23 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0122_monedadenominacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasacambio',
            name='tipo_taca',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Tipo de la Tasa de Cambio'),
        ),
    ]