# Generated by Django 4.0.4 on 2022-06-01 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0034_alter_ciudad_options_alter_tipoempresa_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iva',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='ruta',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='sector',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='subfamilia',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='zona',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='ruta',
            name='codi_vend',
        ),
    ]