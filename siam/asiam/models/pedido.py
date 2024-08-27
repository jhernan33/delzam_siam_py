from .base import Base
from django.db import models
from asiam.models import Cliente
from django.contrib.auth.models import User

class Pedido(Base):
    codi_clie = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='order_customer_code'
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
    foto_pedi = models.JSONField  ('Foto del Pedido',null=True, blank=True)
    codi_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='PedidoUser.codi_user+',
        default=1
    )
    nufa_pedi = models.CharField('Numero de Factura del Pedido', max_length=75, null=True, blank=True)
    mopo_pedi = models.DecimalField ('Monto Porcentaje del Descuento del Pronto Pago Pedido',max_digits=7,decimal_places=2,null=True, blank=True,default=20)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido"'
    
    def get_queryset():
        return Pedido.objects.all().filter(deleted__isnull=True)
    
    """ Check Order Exist """
    def checkOrder(orderId):
        querysetOrder = []
        if orderId is not None:
            queryset = Pedido.get_queryset().filter(id = orderId)
            if queryset.count() > 0:
                querysetOrder = queryset
        return querysetOrder

    """ Get Instance Pedido """
    def getInstanceOrder(Id):
        return Pedido.objects.get(id = Id)
    
    """ Get Data Order Filter By Id """
    def getOrderFilterById(Id:int,show:bool):
        from asiam.models import Moneda, PedidoEstatus, PedidoTipo, PedidoDetalle
        from asiam.serializers import PedidoDetalleBasicSerializer, UserBasicSerializer
        #   Declarate Dict
        result_order = {}
        queryset = Pedido.objects.filter(id = Id) if show == True else Pedido.get_queryset().filter(id = Id)
        if queryset.count() > 0 :
            for k in queryset.iterator():
                result_order['customer_id'] = k.codi_clie
                result_order['customer_all'] = Cliente.searchTypeCustomerId(k.codi_clie.id)
                result_order['customer_without_rif'] = Cliente.searchTypeCustomerIdWithoutRIF(k.codi_clie.id)
                result_order['customer_address'] = Cliente.searchAddressCustomer(k.codi_clie.id)
                result_order['customer_city'] = Cliente.searchCityCustomerId(k.codi_clie.id)
                # Search Contact Customer
                result_order['customer_phone'] = Cliente.searchPhoneCustomer(k.codi_clie.id)
                result_order['invoice_number'] = 'S/N' if k.nufa_pedi is None else k.nufa_pedi
                result_order['order_date'] = k.fech_pedi
                result_order['print_date'] = k.feim_pedi
                result_order['shipping_date'] = k.fede_pedi
                result_order['expiration_date'] = k.feve_pedi
                result_order['observations'] = k.obse_pedi
                result_order['currency_id'] = k.codi_mone.id
                # All Currency
                result_order['currency_all'] = Moneda.searchCurrencyById(k.codi_mone.id).values()
                result_order['amount'] = k.mont_pedi
                result_order['discount'] = k.desc_pedi
                result_order['total_amount'] = k.tota_pedi
                result_order['pourcentage'] = k.mopo_pedi
                # State Order
                result_order['order_state_id'] = k.codi_espe.id
                result_order['order_state_all'] = PedidoEstatus.searchOrderStateById(k.codi_espe.id).values()
                # Type Order
                result_order['type_order_id'] = k.codi_tipe.id
                result_order['type_order_all'] = PedidoTipo.searchOrderTypeById(k.codi_tipe.id).values()
                # Detail
                queryset = PedidoDetalle.searchDetailOrderById(k.id)
                result_detail = PedidoDetalleBasicSerializer(queryset, many=True).data
                result_order['detail'] = result_detail
                # User Create
                querysetUser = User.objects.filter(id = k.codi_user.id)
                result_order['user'] = UserBasicSerializer(querysetUser, many=True).data
        return result_order
