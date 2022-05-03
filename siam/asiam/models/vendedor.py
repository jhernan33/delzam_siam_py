from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class Vendedor(Base):
    fein_vend = models.DateField  ('Fecha de Ingreso del Vendedor',auto_now=False, auto_now_add=False)
    foto_vend = models.JSONField  ('Foto del Vendedor',null=True, blank=True)
    codi_natu = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='natural',
    )

    class Meta:
        ordering = ['codi_natu']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"vendedor"'
