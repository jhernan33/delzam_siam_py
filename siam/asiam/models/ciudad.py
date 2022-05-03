
from .base import Base
from django.db import models

class Ciudad(Base):
    nomb_ciud = models.CharField    ('nomb_ciud',  max_length=200, null=False, blank=False, default='', unique=True)
    codi_esta = models.ForeignKey(
        'Estado',
        on_delete=models.CASCADE,
        related_name='Estado',
    )

    class Meta:
        ordering = ['nomb_ciud']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"ciudad"'
