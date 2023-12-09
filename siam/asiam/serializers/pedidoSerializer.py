import os
from typing import List
from rest_framework import serializers
from asiam.models import Pedido,Cliente, Moneda, PedidoEstatus, PedidoDetalle, PedidoTipo

from django.conf import settings
from django.conf.urls.static import static


class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentOrder = os.path.realpath(settings.WEBSERVER_CUSTOMER)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentOrder+obj['image']
            return value

    def to_internal_value(self, data):
        return data
    
class PedidoSerializer(serializers.ModelSerializer):
    foto_pedi = JSONSerializerField()
    
    class Meta:
        model = Pedido
        field = ('id','codi_mone','deleted')
        exclude =['created','updated','esta_ttus','nufa_pedi','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi','codi_espe','codi_tipe','codi_user']
    
    def to_representation(self, instance):

        representation = super().to_representation(instance)
        querysetPedido = {}
        # Method Search Get Order By Id
        querysetPedido = Pedido.getOrderFilterById(instance.id,False if instance.deleted is None else True)
        if len(querysetPedido) > 0:
            representation['customer_id'] = querysetPedido.get('customer_id').id
            representation['customer_all'] = querysetPedido.get('customer_all')
            representation['customer_without_rif'] = querysetPedido.get('customer_without_rif')
            representation['customer_city'] = querysetPedido.get('customer_city')
            representation['invoice_number'] = querysetPedido.get('invoice_number')
            representation['order_date'] = querysetPedido.get('order_date')
            representation['print_date'] = querysetPedido.get('print_date')
            representation['shipping_date'] = querysetPedido.get('shipping_date')
            representation['expiration_date'] = querysetPedido.get('expiration_date')
            representation['observations'] = querysetPedido.get('observations')
            representation['currency_id'] = querysetPedido.get('currency_id')
            # All Currency
            representation['currency_all'] = querysetPedido.get('currency_all')
            representation['amount'] = querysetPedido.get('amount')
            representation['discount'] = querysetPedido.get('discount')
            representation['total_amount'] = querysetPedido.get('total_amount')
            representation['pourcentage'] = querysetPedido.get('pourcentage')
            # State Order
            representation['order_state_id'] = querysetPedido.get('order_state_id')
            representation['order_state_all'] = querysetPedido.get('order_state_all')
            # Type Order
            representation['type_order_id'] = querysetPedido.get('type_order_id')
            representation['type_order_all'] = querysetPedido.get('type_order_all')
            # Detail
            representation['detail'] = querysetPedido.get('detail')
            # User Create
            representation['user'] = querysetPedido.get('user')

        return representation
    
    """
        Validate Customer Id
    """    
    def validate_customer(value):
        queryset = Cliente.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    
    '''
        Validate Customer and Invoice Number
    '''
    def validate_customer_invoice_number(customerId,invoiceNumber,_id:None):
        invoiceNumber = str(invoiceNumber).upper().split()
        if _id is not None:
            queryset = Pedido.get_queryset().filter(codi_clie = customerId).filter(nufa_pedi =invoiceNumber).exclude(id=_id)
        else:
            queryset = Pedido.get_queryset().filter(codi_clie = customerId).filter(nufa_pedi =invoiceNumber)

        if queryset.count() == 0:
            return False
        else:
            return True
        
class PedidoComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','codi_clie','deleted','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi','foto_pedi','codi_mone','codi_espe','codi_tipe','codi_user']

    def to_representation(self, instance):
        # Serializers
        from asiam.serializers import ClienteComboSerializer
        data = super(PedidoComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["customer"] = ClienteComboSerializer(Cliente.get_queryset().filter(id = instance.codi_clie.id), many=True).data
        return data
    
class PedidoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        field = ('id','codi_clie')
        exclude = ['created','updated','esta_ttus']

class PedidoHistoricoSerializer(serializers.ModelSerializer):
    tota_pedi = serializers.DecimalField(max_digits=7, decimal_places=2)
    
    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Debe ingresar un valor númerico correcto")
        return data
    
    class Meta:
        model = Pedido
        field = ('id','codi_mone')
        exclude =['created','deleted','updated','esta_ttus','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi','codi_espe','codi_tipe','codi_user']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        querysetPedido = {}
        # Method Search Get Order By Id
        querysetPedido = Pedido.getOrderFilterById(instance.id,False if instance.deleted is None else True)
        if len(querysetPedido) > 0:
            representation['customer_id'] = querysetPedido.get('customer_id').id
            representation['customer_all'] = querysetPedido.get('customer_all')
            representation['customer_without_rif'] = querysetPedido.get('customer_without_rif')
            representation['customer_city'] = querysetPedido.get('customer_city')
            representation['invoice_number'] = querysetPedido.get('invoice_number')
            representation['order_date'] = querysetPedido.get('order_date')
            representation['print_date'] = querysetPedido.get('print_date')
            representation['shipping_date'] = querysetPedido.get('shipping_date')
            representation['expiration_date'] = querysetPedido.get('expiration_date')
            representation['observations'] = querysetPedido.get('observations')
            representation['currency_id'] = querysetPedido.get('currency_id')
            # All Currency
            representation['currency_all'] = querysetPedido.get('currency_all')
            representation['amount'] = querysetPedido.get('amount')
            representation['discount'] = querysetPedido.get('discount')
            representation['total_amount'] = querysetPedido.get('total_amount')
            representation['pourcentage'] = querysetPedido.get('pourcentage')
            # State Order
            representation['order_state_id'] = querysetPedido.get('order_state_id')
            representation['order_state_all'] = querysetPedido.get('order_state_all')
            # Type Order
            representation['type_order_id'] = querysetPedido.get('type_order_id')
            representation['type_order_all'] = querysetPedido.get('type_order_all')
            # Detail
            representation['detail'] = querysetPedido.get('detail')
            # User Create
            representation['user'] = querysetPedido.get('user')
        return representation

class PedidoReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pedido
        field = ('id')
        exclude =['created','deleted','updated','esta_ttus'
                ,'codi_mone','codi_clie','fech_pedi','feim_pedi'
                ,'fede_pedi','feve_pedi','mont_pedi','desc_pedi'
                ,'tota_pedi','obse_pedi','orig_pedi','codi_espe'
                ,'codi_tipe','codi_user','foto_pedi','nufa_pedi'
                ,'mopo_pedi'
                ]