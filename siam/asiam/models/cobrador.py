from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class Cobrador(Base):
    codi_natu = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='cobrador.codi_natu+',
    )
    fein_cobr = models.DateField  ('Fecha de Ingreso del Cobrador',auto_now=False, auto_now_add=False,blank=True, null=True)
    foto_cobr = models.JSONField  ('Foto del Cobrador',null=True, blank=True)
    lice_cobr = models.BooleanField('Posee Licencia de Conducir el Cobrador', null=True, blank=True, default=False)
    feli_cobr = models.DateField  ('Fecha de Expedicion de la Licencia del Cobrador',auto_now=False, auto_now_add=False,blank=True, null=True)
    fvli_cobr = models.DateField  ('Fecha de Vencimiento de la Licencia del Cobrador',auto_now=False, auto_now_add=False,blank=True, null=True)
    tili_cobr = models.IntegerField ('Tipo de Licencia del Cobrador',null=True, blank=True, default=1)
    
    class Meta:
        ordering = ['codi_natu']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"cobrador"'

    def get_queryset():
        return Cobrador.objects.all().filter(deleted__isnull=True)
    
    def validate_codi_natu(data,key):
        queryset = Cobrador.objects.filter(codi_natu = data['codi_natu'])
        if queryset.count() == 0:
            return True
        else:
            # Check id 
            if queryset[0].id == key:
                return True
            else:
                return False
    
    """ Is DebtCollector """
    def isDebtCollector(Id):
        resultQuerySetDebtCollector = Cobrador.get_queryset().filter(codi_natu = Id)
        return False if resultQuerySetDebtCollector.count() <= 0 else True