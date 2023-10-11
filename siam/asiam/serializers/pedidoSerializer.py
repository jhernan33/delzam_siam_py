import os
from typing import List
from rest_framework import serializers
from asiam.models import Pedido,Cliente, Moneda, PedidoEstatus, PedidoDetalle

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
        field = ('id','codi_mone')
        exclude =['created','deleted','updated','esta_ttus','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi','codi_espe','codi_tipe','codi_user']
    
    def to_representation(self, instance):
        # Call Serializers
        from asiam.serializers import PedidoDetalleBasicSerializer, PedidoDetalleSerializer
        from asiam.serializers import UserBasicSerializer
        from django.contrib.auth.models import User

        representation = super().to_representation(instance)
        representation['customer_id'] = instance.codi_clie.id
        representation['customer_all'] = Cliente.searchTypeCustomerId(instance.codi_clie.id)
        representation['order_date'] = instance.fech_pedi
        representation['print_date'] = instance.feim_pedi
        representation['shipping_date'] = instance.fede_pedi
        representation['expiration_date'] = instance.feve_pedi
        representation['observations'] = instance.obse_pedi
        representation['currency_id'] = instance.codi_mone.id
        # All Currency
        representation['currency_all'] = Moneda.searchCurrencyById(instance.codi_mone.id).values()
        representation['amount'] = instance.mont_pedi
        representation['discount'] = instance.desc_pedi
        representation['total_amount'] = instance.tota_pedi
        # State
        representation['order_state_id'] = instance.codi_espe.id
        representation['order_state_all'] = PedidoEstatus.searchOrderStateById(instance.codi_espe.id).values()
        # Detail
        queryset = PedidoDetalle.searchDetailOrderById(instance.id)
        result_detail = PedidoDetalleBasicSerializer(queryset, many=True).data
        representation['detail'] = result_detail
        # User Create
        querysetUser = User.objects.filter(id = instance.codi_user.id)
        representation['user'] = UserBasicSerializer(querysetUser, many=True).data
        # print(querysetUser)
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
