from .base import Base
from django.db import models
#Tipos de comunicacion
class Tcomunicaciones(Base):
    desc_tico=models.CharField    ('Descripcion',    max_length=30, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_tico']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"tcomunicaciones"'
