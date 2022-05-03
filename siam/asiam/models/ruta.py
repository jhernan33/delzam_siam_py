from .base import Base
from django.db import models

class Ruta(Base):
    nomb_ruta = models.CharField    ('Nombre de la Ruta', max_length=200, null=True, blank=True, default='', unique=True)
    codi_zona = models.ForeignKey(
        'Zona',
        on_delete=models.CASCADE,
        related_name='Zona',
    )
    codi_vend = models.ForeignKey(
        'Vendedor',
        on_delete=models.CASCADE,
        related_name='Vendedor'
    )

    class Meta:
        ordering = ['nomb_ruta']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"ruta"'
