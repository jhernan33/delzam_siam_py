# Generated by Django 4.0.4 on 2022-06-02 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0039_alter_iva_alic_iva'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articulo',
            options={'ordering': ['desc_arti']},
        ),
        migrations.RenameField(
            model_name='articulo',
            old_name='desc_agen',
            new_name='desc_arti',
        ),
    ]