# Generated by Django 4.1.3 on 2023-10-27 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0105_pedido_nufa_pedi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidoseguimiento',
            name='codi_user',
        ),
    ]