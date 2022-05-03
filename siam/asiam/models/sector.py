from .base import Base
from django.db import models

class Sector(Base):
    nomb_sect = models.CharField    ('Nombre del Sector',    max_length=200, null=False, blank=False, default='', unique=True)
    codi_ciud = models.ForeignKey(
        'Ciudad',
        on_delete=models.CASCADE,
        related_name='Ciudad',
    )

    class Meta:
        ordering = ['nomb_sect']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"sector"'
