# Generated by Django 4.1.3 on 2024-02-03 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0119_pedidopagodetalle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneda',
            name='logo_mone',
            field=models.JSONField(blank=True, null=True, verbose_name='Logo de la Moneda'),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='simb_mone',
            field=models.CharField(blank=True, max_length=120, verbose_name='Simbolo o Abreviatura de la Moneda'),
        ),
    ]