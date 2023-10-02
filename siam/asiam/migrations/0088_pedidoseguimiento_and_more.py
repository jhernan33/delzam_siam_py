# Generated by Django 4.1.3 on 2023-10-02 12:45

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0087_ruta_porc_ruta'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoSeguimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('fech_segu', models.DateField(blank=True, null=True, verbose_name='Fecha del Seguimiento del Pedido')),
                ('foto_segu', models.JSONField(blank=True, null=True, verbose_name='Foto del Seguimiento del Pedido')),
                ('obse_segu', models.TextField(verbose_name='Observaciones del Seguimiento del Pedido')),
                ('location_segu', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('codi_esta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidoPago.codi_esta+', to='asiam.pedidoestatus')),
                ('codi_pedi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidoPago.codi_pedi+', to='asiam.pedido')),
                ('codi_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidoPago.codi_esta+', to='asiam.pedidoestatus')),
            ],
            options={
                'db_table': '"empr"."pedido_seguimiento"',
                'ordering': ['-id'],
            },
        ),
        migrations.AddIndex(
            model_name='pedidoseguimiento',
            index=models.Index(fields=['id'], name='pedido_segu_id_961202_idx'),
        ),
    ]