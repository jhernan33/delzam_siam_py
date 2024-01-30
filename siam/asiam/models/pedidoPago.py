from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class PedidoPago(Base):
    # Forma de Pago, Moneda,
    codi_pedi = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_pedi+'
    )
    codi_esta = models.ForeignKey(
        'PedidoEstatus',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_esta+'
    )
    mont_pago = models.DecimalField ('Monto del Pago',max_digits=7,decimal_places=2,null=True, blank=True)
    obse_pago = models.TextField('Observaciones del Pago',null=True, blank=True)
    fech_pago = models.DateField('Fecha del Pago',auto_now=False, auto_now_add=False,blank=True, null=True)
    topa_pago = models.BooleanField('Total Abono del Pago', null=True, blank=True, default=False)
    
    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_pago"'

    def get_queryset():
        return PedidoPago.objects.all().filter(deleted__isnull=True)