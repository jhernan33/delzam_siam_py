from .base import Base
from django.db import models

class Cuenta(Base):
    ncta_cuen = models.CharField ('Numero de Cuenta',    max_length=50, null=True, blank=True, default='')
    fape_cuen = models.DateField ('Fecha de Creacion de la Cuenta',auto_now=False, auto_now_add=False,blank=True, null=True)
    tipo_cuen = models.CharField ('Tipo de Cuenta',    max_length=25, null=True, blank=True, default='')
    codi_banc = models.ForeignKey(
        'Banco',
        on_delete=models.CASCADE,
        related_name='cuenta.codi_banc+',
    )

    class Meta:
        ordering = ['ncta_cuen']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"cuenta"'

    def get_queryset():
        return Cuenta.objects.all().filter(deleted__isnull=True)