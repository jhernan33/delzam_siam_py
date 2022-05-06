# Generated by Django 4.0.4 on 2022-05-06 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('nomb_esta', models.CharField(default='', max_length=30, unique=True, verbose_name='Nombre del Estado')),
                ('codi_pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pais', to='asiam.pais')),
            ],
            options={
                'db_table': '"comun"."estado"',
                'ordering': ['nomb_esta'],
            },
        ),
        migrations.AddIndex(
            model_name='estado',
            index=models.Index(fields=['id'], name='estado_id_46d099_idx'),
        ),
    ]