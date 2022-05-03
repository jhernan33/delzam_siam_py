from django.db import models
from .base import Base


class Pais(Base):
    nomb_pais=models.CharField    ('Nombre del Pais',    max_length=30, null=False, blank=False, default='', unique=True)

    class Meta:
        ordering = ['nomb_pais']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"pais"'
