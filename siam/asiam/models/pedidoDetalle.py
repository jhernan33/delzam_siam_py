from .base import Base
from django.db import models
from asiam.models import Articulo, Pedido
class PedidoDetalle(Base):
    codi_pedi = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='Pedido.codi_pedi+'
    )
    codi_arti = models.ForeignKey(
        'Articulo',
        on_delete=models.CASCADE,
        related_name='Articulo.codi_arti+'
    )
    cant_pede = models.IntegerField ('Cantidad del Pedido Detalle')
    prec_pede = models.DecimalField ('Precio del Articulo del Pedido Detalle',max_digits=7,decimal_places=2,null=True, blank=True)
    desc_pede = models.DecimalField ('Descuento del Articulo del Pedido Detalle',max_digits=7,decimal_places=2,null=True, blank=True)
    moto_pede = models.DecimalField ('Monto Total del Pedido Detalle',max_digits=7,decimal_places=2,null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"pedido_detalle"'
    
    def get_queryset():
        return PedidoDetalle.objects.all().filter(deleted__isnull=True)
    
    '''
        Check key Exists in Details Items
    '''
    def checkDetails(arg):
        is_many = isinstance(arg,list)
        if is_many:
            for k in arg:
                if k.get('article') is None:
                    return False
                if k.get('quantity') is None:
                    return False
        return True
    
    def saveDictionaryDetail(arg,Order,Customer):
        is_many = isinstance(arg,list)
        if is_many:
            # Create Dictionary Details
            details = dict()
            # print("Customer==>",Customer)
            listDetail = dict()
            # print(type(arg),arg)
            #listDetail = dict(arg)
            for k in arg:
                detail = dict()
                # Create List
                detail['codi_pedi'] = Pedido.get_queryset().get(id = Order)
                detail['codi_arti'] = Articulo.get_queryset().get(id = k['article'])
                detail['cant_pede'] = k['quantity']
                detail['prec_pede'] = k['price']
                detail['desc_pede'] = k['discount']
                detail['moto_pede'] = (k['quantity'] * k['price']) - k['discount']

                # listDetail.update(
                #     {
                #         'codi_pedi': Pedido.get_queryset().get(id = Order),
                #         'codi_arti': Articulo.get_queryset().get(id = k['article']),
                #         'cant_pede': k['quantity']
                #     })
                # item = {'codi_pedi': Pedido.get_queryset().get(id = Order),
                #         'codi_arti': Articulo.get_queryset().get(id = k['article']),
                #         'cant_pede': k['quantity']
                # }
                # listDetail= {**listDetail, **item}
                #details.append(listDetail)
                # print(listDetail,type(listDetail))
            print("Diccionary==>",listDetail)
        return details

    '''
        Search Detail Order By Id
    '''
    def searchDetailOrderById(_id:None):
        queryset_detail = []
        if _id is not None:
            queryset = PedidoDetalle.get_queryset().filter(codi_pedi = _id)
            if queryset.count() > 0:
                queryset_detail = queryset
        return queryset_detail