from .base import Base
from django.db import models

class TasaCambio(Base):
    codi_mone = models.ForeignKey(
        'Moneda',
        on_delete=models.CASCADE,
        related_name='tasacambio.codi_mone+'
    )
    fech_taca = models.DateField ('Fecha de la Tasa de Cambio',auto_now=False, auto_now_add=False,blank=True, null=True)
    obse_taca = models.CharField ('Observaciones de la Tasa de Cmabio', max_length=254, null=True, blank=True, default='')
    esta_tasa = models.BooleanField('Tasa de Cambio Activa', null=True, blank=True, default=True)

    class Meta:
        ordering = ['fech_taca']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"tasa_cambio"'
