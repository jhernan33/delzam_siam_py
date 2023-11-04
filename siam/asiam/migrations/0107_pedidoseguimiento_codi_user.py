# Generated by Django 4.1.3 on 2023-10-27 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asiam', '0106_remove_pedidoseguimiento_codi_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidoseguimiento',
            name='codi_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='PedidoPagoUser.codi_user+', to=settings.AUTH_USER_MODEL),
        ),
    ]