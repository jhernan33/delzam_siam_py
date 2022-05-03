from .base import Base
from django.db import models

class Articulo(Base):
    desc_agen = models.CharField    ('Nombre del Articulo',    max_length=50, null=True, blank=True, default='', unique=True)
    coba_arti = models.CharField    ('Codigo de Barras del Articulo',    max_length=30, null=True, blank=True, default='')
    cmin_arti = models.DecimalField ('Cantidad Minima',max_digits=6,decimal_places=0)
    cmax_arti = models.DecimalField ('Cantidad Maxima',max_digits=6,decimal_places=0)
    por1_arti = models.DecimalField ('Porcentaje de Utilidad 1 Por Articulo',max_digits=7,decimal_places=2)
    por2_arti = models.DecimalField ('Porcentaje de Utilidad 2 Por Articulo',max_digits=7,decimal_places=2)
    por3_arti = models.DecimalField ('Porcentaje de Utilidad 3 Por Articulo',max_digits=7,decimal_places=2)
    ppre_arti = models.DecimalField ('Porcentaje Preferido Por Articulo',max_digits=7,decimal_places=2)
    codi_sufa = models.ForeignKey(
        'SubFamilia',
        on_delete=models.CASCADE,
        related_name='sub_familia',
    )
    foto_arti = models.JSONField()
    codi_ivam = models.ForeignKey(
        'Iva',
        on_delete=models.CASCADE,
        related_name='Iva',
    )
    exgr_arti = models.BooleanField('Exento Grabado del Articulo')
    

    class Meta:
        ordering = ['desc_agen']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"articulo"'
