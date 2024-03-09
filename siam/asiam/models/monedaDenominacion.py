from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class MonedaDenominacion(Base):
    choicesDenomination = (
        ('1','Billete'),
        ('2','Moneda'),
    )
    tipo_deno = models.CharField  ('Tipo de la Denominacion Billete-Moneda', max_length=50, null=False, blank=True, choices = choicesDenomination)
    nomb_deno = models.CharField  ('Nombre de la Denominacion', max_length=120, null=False, blank=False, default='', unique=True)
    valo_deno = models.DecimalField ('Valor de la Denominacion',max_digits=7,decimal_places=2,null=True, blank=True)
    codi_mone = models.ForeignKey(
        'Moneda',
        on_delete=models.CASCADE,
        related_name='monedaDenominacion.codi_mone+'
    )
    foto_deno = models.JSONField  ('Foto de la Denominacion',null=True, blank=True)
    orde_deno = models.IntegerField('Indice de Ordenamiento de la Denominacion',default=1)

    class Meta:
        ordering = ['nomb_deno']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"moneda_denominacion"'

    def get_queryset():
        return MonedaDenominacion.objects.all().filter(deleted__isnull=True)
    
    def searchCurrencyDenominationById(_id:None):
        querysetCurrencyDenomination = []
        if _id is not None:
            queryset = MonedaDenominacion.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                querysetCurrencyDenomination = queryset
        return querysetCurrencyDenomination

    """ Get Instance Currency Denomination """
    def getInstanceCurrencyDenomination(Id):
        return MonedaDenominacion.objects.get(id = Id)