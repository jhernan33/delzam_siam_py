# Generated by Django 4.1.3 on 2023-10-17 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asiam', '0101_remove_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.JSONField(blank=True, null=True, verbose_name='Foto del Perfil'),
        ),
    ]