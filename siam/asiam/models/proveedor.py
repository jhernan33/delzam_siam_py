from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class Proveedor(Base):
    codi_natu = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='natural.codi_natu+'
    )
    codi_juri = models.ForeignKey(
        'Juridica',
        on_delete=models.CASCADE,
        related_name='Juridica.codi_juri+'
    )
    codi_repr = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='natural.codi_natu+'
    ,null=True, blank=True)
    mocr_prov = models.DecimalField ('Monto del Credito',max_digits=7,decimal_places=2)
    plcr_prov = models.IntegerField ('Plazo del del Credito')
    foto_prov = models.JSONField  ('Foto del Proveedor',null=True, blank=True)
    obse_prov = models.TextField('Observaciones del Proveedor',null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"proveedor"'

    def get_queryset():
        return Proveedor.objects.all().filter(deleted__isnull=True)
    
    """ Is Supplier """
    def isSupplier(Id):
        resultQuerySetSupplier = Proveedor.get_queryset().filter(codi_natu = Id)
        return False if resultQuerySetSupplier.count() <= 0 else True