# Generated by Django 4.0.4 on 2022-05-29 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0033_alter_natural_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ciudad',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='tipoempresa',
            options={'ordering': ['-id']},
        ),
    ]