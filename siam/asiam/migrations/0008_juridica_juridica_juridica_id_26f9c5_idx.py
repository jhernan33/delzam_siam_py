# Generated by Django 4.0.4 on 2022-04-29 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0007_tipoempresa_tipoempresa_tipo_empres_id_745ff0_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Juridica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('riff_peju', models.CharField(default='', max_length=10, unique=True, verbose_name='RIF')),
                ('raso_peju', models.CharField(default='', max_length=254, unique=True, verbose_name='Razon Social ')),
                ('dofi_peju', models.TextField(default='', max_length=254, verbose_name='Domicilio Fiscal')),
                ('ivaa_peju', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Paga IVA')),
                ('islr_peju', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Paga ISLR')),
                ('desc_peju', models.TextField(blank=True, default='', max_length=1, null=True, verbose_name='Descripcion')),
                ('fori_peju', models.JSONField(verbose_name='Foto del Rif')),
                ('folo_peju', models.JSONField(verbose_name='Foto del Local')),
                ('pure_peju', models.TextField(verbose_name='Punto de Referencia')),
                ('fevi_peju', models.DateField(verbose_name='Fecha de Vencimiento del RIF')),
                ('codi_ciud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='natural.codi_ciud+', to='asiam.ciudad')),
                ('codi_sect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='natural.codi_sect+', to='asiam.sector')),
                ('codi_tiem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TipoEmpresa', to='asiam.tipoempresa')),
            ],
            options={
                'db_table': '"comun"."juridica"',
                'ordering': ['raso_peju'],
            },
        ),
        migrations.AddIndex(
            model_name='juridica',
            index=models.Index(fields=['id'], name='juridica_id_26f9c5_idx'),
        ),
    ]
