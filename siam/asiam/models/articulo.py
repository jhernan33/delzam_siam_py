from .base import Base
from django.db import models

class Articulo(Base):
    codi_arti = models.CharField    ('Codigo del Articulo SIAE',max_length=50, null=True, blank=True, default='', unique=True)
    idae_arti = models.CharField    ('Codigo del Articulo SIAE',max_length=15, null=True, blank=True)
    desc_arti = models.CharField    ('Nombre del Articulo',    max_length=250, null=True, blank=True, default='', unique=False)
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
    exgr_arti = models.CharField('Exento Grabado del Articulo',max_length=1, null=True, blank=True)
    codc_pres = models.IntegerField('Codigo de Presentacion de Compra')
    codv_pres = models.IntegerField('Codigo de Presentacion de Venta')
    capc_arti = models.IntegerField('Capacidad de Compra del Articulo')
    capv_arti = models.IntegerField('Capacidad de Venta del Articulo')
    proc_arti = models.CharField   ('Codigo del Articulo SIAE',max_length=1, null=True, blank=True, default='')
    codi_ivti = models.ForeignKey(
        'IvaGeneral',
        on_delete=models.CASCADE,
        related_name='ivti_general',
        blank=True, null=True
    )

    class Meta:
        ordering = ['desc_arti']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"articulo"'

    def save(self, **kwargs):
        self.idae_arti = self.idae_arti.upper()
        self.desc_arti = self.desc_arti.upper()
        self.exgr_arti = self.exgr_arti.upper()
        return super().save(**kwargs)

    def get_queryset():
        return Articulo.objects.all().filter(deleted__isnull=True)