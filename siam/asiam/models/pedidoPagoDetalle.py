from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class PedidoPagoDetalle(Base):
    # Codigo del Pago
    codi_pago = models.ForeignKey(
        'PedidoPago',
        on_delete=models.CASCADE,
        related_name='pedidoPagoDetalle.codi_pago+'
    )
    # Forma de Pago
    codi_fopa = models.ForeignKey(
        'FormaPago',
        on_delete=models.CASCADE,
        related_name='pedidoPagoDetalle.codi_fopa+'
    )
    # Estatus del Pago (Pagado, Pendiente)
    codi_esta = models.ForeignKey(
        'PedidoEstatus',
        on_delete=models.CASCADE,
        related_name='pedidoPagoDetalle.codi_esta+'
    )
    # Codigo de la Moneda
    codi_mone = models.ForeignKey(
        'Moneda',
        on_delete=models.CASCADE,
        related_name='pedidoPagoDetalle.codi_mone+'
    )
    # Tasa de Cambio de la Moneda
    codi_tasa = models.ForeignKey(
        'TasaCambio',
        on_delete=models.CASCADE,
        related_name='pedidoPagoDetalle.codi_tasa+'
    )
    # Cobrador
    codi_cobr = models.ForeignKey(
        'Cobrador',
        on_delete=models.CASCADE,
        related_name='pedidoPagoDetalle.codi_cobr+'
    )
    mont_pade = models.DecimalField ('Monto del Pago',max_digits=7,decimal_places=2,null=True, blank=True)
    foto_pade = models.JSONField  ('Foto del Pago',null=True, blank=True)
    obse_pade = models.TextField('Observaciones del Detalle Pago',null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_pago_detalle"'

    def get_queryset():
        return PedidoPagoDetalle.objects.all().filter(deleted__isnull=True)