from .base import Base
from django.db import models

class Moneda(Base):
    desc_mone = models.CharField  ('Descripcion de la Moneda', max_length=120, null=False, blank=False, default='', unique=True)
    codi_pais = models.ForeignKey(
        'Pais',
        on_delete=models.CASCADE,
        related_name='Pais.codi_pais+',
        default='234'
    )
    simb_mone = models.CharField  ('Simbolo de la Moneda', max_length=120, null=False, blank=True)
    codi_mone = models.CharField  ('Codigo de la Moneda', max_length=50, null=False, blank=True)

    class Meta:
        ordering = ['desc_mone']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"moneda"'

    def get_queryset():
        return Moneda.objects.all().filter(deleted__isnull=True)
    
    def searchCurrencyById(_id:None):
        queryset_Currency = []
        if _id is not None:
            queryset = Moneda.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                queryset_Currency = queryset
        return queryset_Currency

    """ Get Instance Currency """
    def getInstanceCurrency(Id):
        return Moneda.objects.get(id = Id)