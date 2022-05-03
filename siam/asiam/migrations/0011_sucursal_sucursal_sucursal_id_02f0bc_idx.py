# Generated by Django 4.0.4 on 2022-04-29 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0010_accionista_accionista_accionista_id_1a2e91_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('dofi_sucu', models.TextField(default='', max_length=254, verbose_name='Domicilio Fiscal de la Sucursal')),
                ('desc_sucu', models.TextField(blank=True, default='', max_length=1, null=True, verbose_name='Descripcion de la Sucursal')),
                ('folo_peju', models.JSONField(blank=True, null=True, verbose_name='Foto del Local')),
                ('pure_peju', models.TextField(verbose_name='Punto de Referencia')),
                ('codi_ciud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='natural.codi_ciud+', to='asiam.sucursal')),
                ('codi_sect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='natural.codi_sect+', to='asiam.sector')),
                ('repr_sucu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Natural.repr_sucu+', to='asiam.natural')),
                ('riff_peju', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Juridica', to='asiam.juridica')),
            ],
            options={
                'db_table': '"comun"."sucursal"',
                'ordering': ['riff_peju'],
            },
        ),
        migrations.AddIndex(
            model_name='sucursal',
            index=models.Index(fields=['id'], name='sucursal_id_02f0bc_idx'),
        ),
    ]
