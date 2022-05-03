
from .base import Base
from django.db import models

class Municipio(Base):
    nomb_muni = models.CharField    ('nomb_muni',    max_length=30, null=False, blank=False, default='', unique=True)
    codi_esta = models.ForeignKey(
        'Estado',
        on_delete=models.CASCADE,
        related_name='Estado',
    )

    class Meta:
        ordering = ['nomb_muni']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"municipio"'
