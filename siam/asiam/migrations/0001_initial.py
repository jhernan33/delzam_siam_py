# Generated by Django 4.0.4 on 2022-04-29 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("create schema if not exists comun"),
        migrations.RunSQL("create schema if not exists empr"),
        migrations.RunSQL("create schema if not exists ppal"),
        migrations.RunSQL("create schema if not exists p2022"),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta_ttus', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='Estatus')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('nomb_pais', models.CharField(default='', max_length=30, unique=True, verbose_name='Nombre del Pais')),
            ],
            options={
                'db_table': '"comun"."pais"',
                'ordering': ['nomb_pais'],
            },
        ),
        migrations.AddIndex(
            model_name='pais',
            index=models.Index(fields=['id'], name='pais_id_0f5e88_idx'),
        ),
    ]
