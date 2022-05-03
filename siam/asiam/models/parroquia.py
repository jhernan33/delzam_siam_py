
from .base import Base
from django.db import models

class Parroquia(Base):
    nomb_parr = models.CharField    ('nomb_parr',    max_length=30, null=False, blank=False, default='', unique=True)
    codi_muni = models.ForeignKey(
        'Municipio',
        on_delete=models.CASCADE,
        related_name='Municipio',
    )
    class Meta:
        ordering = ['nomb_parr']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"parroquia"'
