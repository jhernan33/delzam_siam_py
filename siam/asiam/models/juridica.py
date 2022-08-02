from .base import Base
from django.contrib.postgres.fields import JSONField
from django.db import models

class Juridica(Base):
    riff_peju = models.CharField   ('RIF',    max_length=12, null=False, blank=False, default='',unique=True)
    raso_peju = models.CharField   ('Razon Social ',    max_length=254, null=False, blank=False, default='', unique=True)
    dofi_peju = models.TextField   ('Domicilio Fiscal',    max_length=254, null=False, blank=False, default='')
    ivaa_peju = models.CharField   ('Paga IVA',    max_length=1, null=True, blank=True, default='')
    islr_peju = models.CharField   ('Paga ISLR',    max_length=1, null=True, blank=True, default='')
    desc_peju = models.TextField   ('Descripcion',    max_length=1, null=True, blank=True, default='')
    codi_tiem = models.ForeignKey(
        'TipoEmpresa',
        on_delete=models.CASCADE,
        related_name='TipoEmpresa',
    )
    codi_ciud = models.ForeignKey(
        'Ciudad',
        on_delete=models.CASCADE,
        related_name='natural.codi_ciud+',
    )
    codi_sect = models.ForeignKey(
        'Sector',
        on_delete=models.CASCADE,
        related_name='natural.codi_sect+',
    )
    fori_peju = models.JSONField('Foto del Rif',null=True, blank=True)
    folo_peju = models.JSONField('Foto del Local',null=True, blank=True)
    pure_peju = models.TextField('Punto de Referencia')
    fevi_peju = models.DateField('Fecha de Vencimiento del RIF')
    
    class Meta:
        ordering = ['raso_peju']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"juridica"'
    
    
    def get_queryset():
        return Juridica.objects.all().filter(deleted__isnull=True)
