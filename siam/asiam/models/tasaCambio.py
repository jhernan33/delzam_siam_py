from .base import Base
from django.db import models

class TasaCambio(Base):
    codi_mone = models.ForeignKey(
        'Moneda',
        on_delete=models.CASCADE,
        related_name='moneda.codi_mone+'
    )
    fech_taca = models.DateTimeField ('Fecha de la Tasa de Cambio',auto_now=False, auto_now_add=False,blank=True, null=True)
    valo_taca = models.DecimalField ('Valor de la Tasa de Cambio',max_digits=7,decimal_places=2,default=1)
    obse_taca = models.CharField ('Observaciones de la Tasa de Cmabio', max_length=254, null=True, blank=True, default='')

    class Meta:
        ordering = ['fech_taca']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"tasa_cambio"'

    def get_queryset():
        return TasaCambio.objects.all().filter(deleted__isnull=True)
    
    """ Get Instance Exchange Rate """
    def getInstanceExchangeRate(Id):
        return TasaCambio.objects.get(id = Id)

    # Filter Exchange Rate by Currency Id
    def filterByCurrencyId(CurrencyId):
        return TasaCambio.get_queryset().filter(codi_mone = CurrencyId)