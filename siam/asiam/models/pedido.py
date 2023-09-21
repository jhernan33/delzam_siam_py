from .base import Base
from django.db import models
from asiam.models import Cliente
class Pedido(Base):
    codi_clie = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='Cliente.codi_clie+'
    )
    fech_pedi = models.DateField('Fecha de creacion del Pedido',auto_now=False, auto_now_add=False,blank=True, null=True)
    feim_pedi = models.DateField('Fecha de Impresion del Pedido',auto_now=False, auto_now_add=False,blank=True, null=True)
    fede_pedi = models.DateField('Fecha de Despacho del Pedido',auto_now=False, auto_now_add=False,blank=True, null=True)
    feve_pedi = models.DateField('Fecha de Vencimiento del Pedido',auto_now=False, auto_now_add=False,blank=True, null=True)
    mont_pedi = models.DecimalField ('Monto del Pedido sin Descuento',max_digits=7,decimal_places=2,null=True, blank=True)
    desc_pedi = models.DecimalField ('Monto del Descuento del Pedido',max_digits=7,decimal_places=2,null=True, blank=True)
    tota_pedi = models.DecimalField ('Monto Total del Pedido',max_digits=7,decimal_places=2,null=True, blank=True)
    obse_pedi = models.TextField('Observaciones del Pedido')
    orig_pedi = models.TextField('Origen de donde fue creado el Pedido')
    codi_mone = models.ForeignKey(
        'Moneda',
        on_delete = models.CASCADE,
        related_name="Moneda.codi_mone+",
    )
    codi_espe = models.ForeignKey(
        'PedidoEstatus',
        on_delete = models.CASCADE,
        related_name='PedidoEstatus.codi_espe+'
    )
    codi_tipe = models.ForeignKey(
        'PedidoTipo',
        on_delete = models.CASCADE,
        related_name='PedidoTipo.codi_tipe+'
    )

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido"'
    
    def get_queryset():
        return Pedido.objects.all().filter(deleted__isnull=True)

    # Restore Id Deleted
    def restoreNatural(key):
        Pedido.objects.filter(id=key).update(deleted =None)
    