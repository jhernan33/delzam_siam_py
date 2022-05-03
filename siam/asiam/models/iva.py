from .base import Base
from django.db import models

class Iva(Base):
    alic_iva = models.IntegerField ('Alicuota',   null=True, blank=True, default=0)
    fini_iva = models.DateField    ('Entra VIgencia')
    ffin_iva = models.DateField    ('Fin de Vigencia')

    class Meta:
        ordering = ['fini_iva']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"iva"'
