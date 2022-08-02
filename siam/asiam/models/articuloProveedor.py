from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class ArticuloProveedor(Base):
    codi_arti = models.ForeignKey(
        'Articulo',
        on_delete=models.CASCADE,
        related_name='articulo.id+'
    )
    codi_prov = models.ForeignKey(
        'Proveedor',
        on_delete=models.CASCADE,
        related_name='Proveedor.codi_prov+'
    )
    codi_arti_prov = models.CharField ('Codigo del Articulo Proveedor', max_length=50, null=True, blank=True)
    obse_arti_prov = models.TextField('Observaciones del Proveedor',null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"articulo_proveedor"'
    
    def save(self, **kwargs):
        self.obse_arti_prov = self.obse_arti_prov.upper().strip()
        return super(ArticuloProveedor,self).save(**kwargs)

    def get_queryset():
        return ArticuloProveedor.objects.all().filter(deleted__isnull=True)