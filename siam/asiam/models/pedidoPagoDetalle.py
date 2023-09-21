from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class PedidoPagoDetalle(Base):
    # Forma de Pago, Moneda,
    codi_pedi = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_pedi+'
    )
    codi_fopa = models.ForeignKey(
        'FormaPago',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_fopa+'
    )
    codi_mone = models.ForeignKey(
        'Moneda',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_mone+'
    )
    codi_esta = models.ForeignKey(
        'PedidoEstatus',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_esta+'
    )
    mont_fopa = models.DecimalField ('Monto de la Forma de Pago',max_digits=7,decimal_places=2,null=True, blank=True)
    foto_fopa = models.JSONField  ('Foto del Cliente',null=True, blank=True)
    obse_fopa = models.TextField('Observaciones de la Forma de Pago')

    

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_pago_detalle"'

    def get_queryset():
        return PedidoPagoDetalle.objects.all().filter(deleted__isnull=True)