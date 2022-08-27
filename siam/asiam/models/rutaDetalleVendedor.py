import imp
from .base import Base
from django.db import models

class RutaDetalleVendedor(Base):
    codi_ruta = models.ForeignKey(
        'Ruta',
        on_delete=models.CASCADE,
        related_name='Ruta',
    )
    codi_vend = models.ForeignKey(
        'Vendedor',
        on_delete=models.CASCADE,
        related_name='Vendedor',
    )

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"ruta_detalle_vendedor"'
        unique_together = ('codi_ruta','codi_vend')
    
    def get_queryset():
        return RutaDetalleVendedor.objects.all().filter(deleted__isnull=True)
    
    """
    Method List Seller from Router
    Self Id
    """    
    def listSellerRoute(self):
        queryset = RutaDetalleVendedor.objects.filter(codi_ruta=self.id)
        # print(queryset)
        return queryset
        #return "id="+str(self.id)

    # def __str__(self):
    #     return '%d: %d' % (self.codi_ruta, self.codi_vend)
