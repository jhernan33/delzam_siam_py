from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models

class PedidoSeguimiento(Base):
    codi_pedi = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_pedi+'
    )
    # Pendiente, Pagado, Anulado, Camino
    codi_esta = models.ForeignKey(
        'PedidoEstatus',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_esta+'
    )
    codi_user = models.ForeignKey(
        'PedidoEstatus',
        on_delete=models.CASCADE,
        related_name='pedidoPago.codi_esta+'
    )
    fech_segu = models.DateField('Fecha del Seguimiento del Pedido',auto_now=False, auto_now_add=False,blank=True, null=True)
    foto_segu = models.JSONField  ('Foto del Seguimiento del Pedido',null=True, blank=True)
    obse_segu = models.TextField('Observaciones del Seguimiento del Pedido')
    location_segu = models.PointField(srid=4326, null=True, blank=True)
    

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_seguimiento"'

    def get_queryset():
        return PedidoSeguimiento.objects.all().filter(deleted__isnull=True)