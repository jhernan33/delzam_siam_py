from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class Cliente(Base):
    fein_clie = models.DateField  ('Fecha de Ingreso del Cliente',auto_now=False, auto_now_add=False,blank=True, null=True)
    codi_ante = models.IntegerField('Codigo Anterior',null=True, blank=True)
    cred_clie = models.BooleanField('Credito del Cliente')
    mocr_clie = models.DecimalField ('Monto del Credito',max_digits=7,decimal_places=2)
    plcr_clie = models.IntegerField ('Plazo del del Credito')
    prde_clie = models.DecimalField ('Porcentage de Descuento',max_digits=7,decimal_places=2)
    prau_clie = models.DecimalField ('Porcentage de Aumento',max_digits=7,decimal_places=2)

    codi_vend = models.ForeignKey(
        'Vendedor',
        on_delete=models.CASCADE,
        related_name='Vendedor.codi_vend+'
    )
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
    foto_clie = models.JSONField  ('Foto del Cliente',null=True, blank=True)

    class Meta:
        ordering = ['codi_natu']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"cliente"'
