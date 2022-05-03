from .base import Base
from django.db import models

class Profesiones(Base):
    desc_prof=models.CharField    ('Descripcion',    max_length=50, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_prof']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"profesiones"'
