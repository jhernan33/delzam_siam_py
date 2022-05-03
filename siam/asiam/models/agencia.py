from .base import Base
from django.db import models

class Agencia(Base):
    desc_agen=models.CharField    ('Nombre de la Agencia',    max_length=50, null=True, blank=True, default='', unique=True)
    dire_agen=models.TextField    ('Direccion de la Agencia',    max_length=1, null=True, blank=True, default='')
    codi_banc = models.ForeignKey(
        'Banco',
        on_delete=models.CASCADE,
        related_name='Banco_a',
    )

    class Meta:
        ordering = ['desc_agen']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"agencia"'
