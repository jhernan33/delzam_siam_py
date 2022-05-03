from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField
class Sucursal(Base):
    dofi_sucu = models.TextField   ('Domicilio Fiscal de la Sucursal',    max_length=254, null=False, blank=False, default='')
    desc_sucu = models.TextField   ('Descripcion de la Sucursal',    max_length=1, null=True, blank=True, default='')

    riff_peju = models.ForeignKey(
        'Juridica',
        on_delete=models.CASCADE,
        related_name='Juridica',
    )
    codi_ciud = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        related_name='natural.codi_ciud+',
    )
    codi_sect = models.ForeignKey(
        'Sector',
        on_delete=models.CASCADE,
        related_name='natural.codi_sect+',
    )
    repr_sucu = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='Natural.repr_sucu+',
    )
    folo_peju = models.JSONField('Foto del Local',null=True, blank=True)
    pure_peju = models.TextField('Punto de Referencia')
    
    class Meta:
        ordering = ['riff_peju']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"sucursal"'
