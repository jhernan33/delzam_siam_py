from .base import Base
from django.db import models

class Presupuesto(Base):
    desc_prep=models.CharField    ('Descripcion',    max_length=75, null=True, blank=True, default='', unique=True)
    anos_prep=models.IntegerField ('Año',   null=True, blank=True, default=0)

    class Meta:
        ordering = ['desc_prep']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"presupuesto"'
