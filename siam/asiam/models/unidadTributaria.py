from .base import Base
from django.db import models

class UnidadTributaria(Base):
    mont_untr = models.DecimalField ('Monto', max_digits=12, decimal_places=4,  null=False, blank=False, default=0)
    fini_untr = models.DateField    ('Entrada en vigencia')
    ffin_untr = models.DateField    ('Final de la Vigencia')

    class Meta:
        ordering = ['fini_untr']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"unidad_tributaria"'
