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
    
    """ Get Instance Tipo Pedido """
    def getInstanceOrderType(Id):
        return PedidoTipo.objects.get(id = Id)
    
    '''
        Search Order Type by Id
    '''
    def searchOrderTypeById(_id:None):
        queryset_order_type = []
        if _id is not None:
            queryset = PedidoTipo.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                queryset_order_type = queryset
        return queryset_order_type

    def __str__(self): # new
        return str(self.desc_tipe).upper().strip()