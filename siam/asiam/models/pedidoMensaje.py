from .base import Base
from django.db import models

class PedidoMensaje(Base):
    desc_mens = models.CharField('Descripcion del Mensaje', max_length=254, null=True, blank=True)
    # Pedido, Factura, Proforma, Nota de Credito
    codi_tipe = models.ForeignKey(
        'PedidoTipo',
        on_delete = models.CASCADE,
        related_name='MensajeTipo.codi_tipe+'
    )
    pred_mens = models.BooleanField('Predeterminado Mensaje', null=True, blank=True, default=False)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_mensaje"'

    def get_queryset():
        return PedidoMensaje.objects.all().filter(deleted__isnull=True)
    
    def save(self, **kwargs):
        self.desc_mens = self.desc_mens.lower().strip()
        return super(PedidoMensaje,self).save(**kwargs)
    
    def validate_desc_mens(value):
        queryset = PedidoMensaje.objects.filter(desc_mens = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    
    """ Get Instance Tipo Pedido """
    def getInstanceOrderType(Id):
        return PedidoMensaje.objects.get(id = Id)
    
    '''
        Search Order Type by Id
    '''
    def searchOrderTypeById(_id:None):
        queryset_order_type = []
        if _id is not None:
            queryset = PedidoMensaje.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                queryset_order_type = queryset
        return queryset_order_type

    def __str__(self): # new
        return str(self.desc_mens).upper().strip()