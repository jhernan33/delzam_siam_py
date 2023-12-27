# Generated by Django 4.1.3 on 2023-12-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0113_alter_articulo_ppre_arti'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='por1_arti',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='Porcentaje de Utilidad 1 Por Articulo'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='por2_arti',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='Porcentaje de Utilidad 2 Por Articulo'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='por3_arti',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='Porcentaje de Utilidad 3 Por Articulo'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='por4_arti',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, verbose_name='Porcentaje de Utilidad 4 Por Articulo'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='ppre_arti',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, verbose_name='Porcentaje Preferido Por Articulo'),
        ),
    ]
