# Generated by Django 4.0.4 on 2022-06-02 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0036_rutadetallevendedor_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rutadetallevendedor',
            unique_together={('codi_ruta', 'codi_vend')},
        ),
    ]