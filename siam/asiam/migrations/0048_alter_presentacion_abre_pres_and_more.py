# Generated by Django 4.0.4 on 2022-06-17 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0047_presentacion_presentacion_presentacio_id_88eafc_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentacion',
            name='abre_pres',
            field=models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='abre_pres'),
        ),
        migrations.AlterField(
            model_name='presentacion',
            name='tipo_pres',
            field=models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='tipo_pres'),
        ),
    ]
