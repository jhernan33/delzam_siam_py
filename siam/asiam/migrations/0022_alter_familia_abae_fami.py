# Generated by Django 4.0.4 on 2022-05-06 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0021_moneda_moneda_moneda_id_e8ef9d_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familia',
            name='abae_fami',
            field=models.CharField(blank=True, default='', max_length=3, null=True, verbose_name='abae_fami'),
        ),
    ]
