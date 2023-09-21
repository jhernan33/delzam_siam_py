from .base import Base
from django.db import models

class PedidoEstatus(Base):
    # Pendiente, Pagado, Anulado
    desc_esta = models.CharField('Descripcion del Estatus del Pedido', max_length=200, null=True, blank=True)
    orde_esta = models.IntegerField ('Orden del Estatus del Pedido')

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_estatus"'

    def get_queryset():
        return PedidoEstatus.objects.all().filter(deleted__isnull=True)