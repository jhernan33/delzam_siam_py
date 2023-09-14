from .base import Base
from django.db import models
from asiam.models import Articulo
class PedidoDetalle(Base):
    codi_pedi = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='Pedido.codi_pedi+'
    )
    codi_arti = models.ForeignKey(
        'Articulo',
        on_delete=models.CASCADE,
        related_name='Articulo.codi_arti+'
    )
    cant_pede = models.IntegerField ('Cantidad del Pedido Detalle')
    prec_pede = models.DecimalField ('Precio del Articulo del Pedido Detalle',max_digits=7,decimal_places=2,null=True, blank=True)
    desc_pede = models.DecimalField ('Descuento del Articulo del Pedido Detalle',max_digits=7,decimal_places=2,null=True, blank=True)
    moto_pede = models.DecimalField ('Monto Total del Pedido Detalle',max_digits=7,decimal_places=2,null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_detalle"'
    
    def get_queryset():
        return PedidoDetalle.objects.all().filter(deleted__isnull=True)