# Generated by Django 4.0.4 on 2022-06-01 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0035_alter_iva_options_alter_ruta_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RutaDetalleVendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('codi_ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ruta', to='asiam.ruta')),
                ('codi_vend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Vendedor', to='asiam.vendedor')),
            ],
            options={
                'db_table': '"empr"."ruta_detalle_vendedor"',
                'ordering': ['-id'],
            },
        ),
        migrations.AddIndex(
            model_name='rutadetallevendedor',
            index=models.Index(fields=['id'], name='ruta_detall_id_9fd97c_idx'),
        ),
    ]