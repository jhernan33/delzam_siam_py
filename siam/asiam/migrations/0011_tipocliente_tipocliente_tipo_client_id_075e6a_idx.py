# Generated by Django 4.0.4 on 2022-05-06 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0010_sucursal_sucursal_sucursal_id_02f0bc_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipocliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('desc_ticl', models.CharField(blank=True, default='', max_length=120, null=True, unique=True, verbose_name='Descripcion del Tipo de Cliente')),
            ],
            options={
                'db_table': '"comun"."tipo_cliente"',
                'ordering': ['desc_ticl'],
            },
        ),
        migrations.AddIndex(
            model_name='tipocliente',
            index=models.Index(fields=['id'], name='tipo_client_id_075e6a_idx'),
        ),
    ]