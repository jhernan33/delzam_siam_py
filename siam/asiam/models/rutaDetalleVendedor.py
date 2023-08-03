import imp
from .base import Base
from django.db import models
from asiam.models import Vendedor, Natural

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
        return queryset
        #return "id="+str(self.id)

    # def __str__(self):
    #     return '%d: %d' % (self.codi_ruta, self.codi_vend)

    

    """
    Search Seller
    """
    def searchSeller(self):
        _result_detail = RutaDetalleVendedor.objects.filter(id = self.id).values("codi_vend")
        _result_seller = Vendedor.objects.filter(id = _result_detail[0]['codi_vend']).values('codi_natu')
        _result_natural = Natural.objects.filter(id = _result_seller[0]['codi_natu'])
        return str(_result_natural[0].prno_pena[0]+"."+_result_natural[0].seno_pena[0]+"."+_result_natural[0].prap_pena[0]+"."+_result_natural[0].seap_pena[0]).strip().upper()

    # Search Route and Zone
    def searchRouteZone(self):
        from asiam.models import Ruta
        #_result_route = Ruta.get_queryset().filter(self.)
        #for k in self:
            #_ruta = k.get('codi_ruta')
        # print(self.id)
        _ruta = RutaDetalleVendedor.objects.filter(id = self.id).values("codi_ruta")
        # print(_ruta[0]['codi_ruta'])
        _querysetRoute = Ruta.objects.filter(id = _ruta[0]['codi_ruta']).select_related('codi_zona').all()  #.values('nomb_ruta','codi_zona','codi_zona.desc_zona')
        # print(_querysetRoute[0].nomb_ruta,_querysetRoute[0].codi_zona.desc_zona)
        return _querysetRoute