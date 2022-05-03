from .base import Base
from django.db import models

class Moneda(Base):
    desc_mone = models.CharField  ('Descripcion de la Moenda',    max_length=120, null=False, blank=False, default='', unique=True)

    class Meta:
        ordering = ['desc_mone']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"moneda"'
