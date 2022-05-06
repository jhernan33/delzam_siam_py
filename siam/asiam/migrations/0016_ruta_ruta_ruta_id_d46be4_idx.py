# Generated by Django 4.0.4 on 2022-05-06 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0015_vendedor_vendedor_vendedor_id_5cac0b_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('nomb_ruta', models.CharField(blank=True, default='', max_length=200, null=True, unique=True, verbose_name='Nombre de la Ruta')),
                ('codi_vend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Vendedor', to='asiam.vendedor')),
                ('codi_zona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Zona', to='asiam.zona')),
            ],
            options={
                'db_table': '"empr"."ruta"',
                'ordering': ['nomb_ruta'],
            },
        ),
        migrations.AddIndex(
            model_name='ruta',
            index=models.Index(fields=['id'], name='ruta_id_d46be4_idx'),
        ),
    ]