# Generated by Django 4.0.4 on 2022-05-13 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0026_alter_subfamilia_options_remove_subfamilia_desc_sufa'),
    ]

    operations = [
        migrations.AddField(
            model_name='subfamilia',
            name='desc_sufa',
            field=models.CharField(default='', max_length=200, verbose_name='desc_sufa'),
        ),
    ]