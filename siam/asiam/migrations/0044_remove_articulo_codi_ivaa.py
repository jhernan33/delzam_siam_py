# Generated by Django 4.0.4 on 2022-06-02 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0043_alter_articulo_desc_arti'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulo',
            name='codi_ivaa',
        ),
    ]
