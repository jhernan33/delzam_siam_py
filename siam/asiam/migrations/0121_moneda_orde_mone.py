# Generated by Django 4.1.3 on 2024-02-06 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0120_moneda_logo_mone_alter_moneda_simb_mone'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneda',
            name='orde_mone',
            field=models.IntegerField(default=1, verbose_name='Indice de Ordenamiento de la Moneda'),
        ),
    ]