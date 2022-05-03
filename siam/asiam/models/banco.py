from .base import Base
from django.db import models

class Banco(Base):
    desc_banc=models.CharField    ('Nombre del Banco',    max_length=50, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_banc']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"banco"'
