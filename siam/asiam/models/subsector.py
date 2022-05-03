from .base import Base
from django.db import models

class SubSector(Base):
    nomb_suse=models.CharField    ('Nombre del Sub Sector',    max_length=30, null=False, blank=False, default='', unique=True)
    codi_sect = models.ForeignKey(
        'Sector',
        on_delete=models.CASCADE,
        related_name='Sector',
    )

    class Meta:
        ordering = ['nomb_suse']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"subsector"'
