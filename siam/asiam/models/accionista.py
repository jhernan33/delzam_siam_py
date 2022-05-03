from .base import Base
from django.db import models

class Accionista(Base):
    codi_acci = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='natural.codi_natu+',
    )
    codi_juri = models.ForeignKey(
        'Juridica',
        on_delete=models.CASCADE,
        related_name='Juridica.codi_juri+',
    )
    fere_acci = models.DateField('Fecha de Registro', null=False, blank=True)


    class Meta:
        ordering = ['codi_acci']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"accionista"'
