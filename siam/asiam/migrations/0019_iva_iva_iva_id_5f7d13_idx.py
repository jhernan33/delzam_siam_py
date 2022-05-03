# Generated by Django 4.0.4 on 2022-04-29 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0018_unidadmedida_unidadmedida_unidad_medi_id_46af74_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('alic_iva', models.IntegerField(blank=True, default=0, null=True, verbose_name='Alicuota')),
                ('fini_iva', models.DateField(verbose_name='Entra VIgencia')),
                ('ffin_iva', models.DateField(verbose_name='Fin de Vigencia')),
            ],
            options={
                'db_table': '"comun"."iva"',
                'ordering': ['fini_iva'],
            },
        ),
        migrations.AddIndex(
            model_name='iva',
            index=models.Index(fields=['id'], name='iva_id_5f7d13_idx'),
        ),
    ]
