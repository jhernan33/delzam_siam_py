from .base import Base
from django.db import models

class PedidoTipo(Base):
    # Pedido, Factura, Proforma, Nota de Credito
    desc_tipe = models.CharField('Descripcion del Tipo de Pedido', max_length=200, null=True, blank=True)
    orde_tipe = models.IntegerField ('Orden del Tipo de Pedido')

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_tipo"'

    def get_queryset():
        return PedidoTipo.objects.all().filter(deleted__isnull=True)
    
    def save(self, **kwargs):
        self.desc_tipe = self.desc_tipe.lower().strip()
        return super(PedidoTipo,self).save(**kwargs)
    
    def validate_desc_tipe(value):
        queryset = PedidoTipo.objects.filter(desc_tipe = value)
        if queryset.count() == 0:
            return False
        else:
            return True