from .base import Base
from django.db import models

class Iva(Base):
    alic_iva = models.DecimalField ('Alicuota', max_digits=8,decimal_places=2,null=True, blank=True, default=0)
    fini_iva = models.DateField    ('Entra VIgencia')
    ffin_iva = models.DateField    ('Fin de Vigencia')

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"iva"'

    def get_queryset():
        return Iva.objects.all().filter(deleted__isnull=True)