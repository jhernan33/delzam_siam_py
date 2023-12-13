from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import PedidoMensaje, PedidoTipo
from asiam.serializers.pedidoTipoSerializer import PedidoTipoBasicSerializer, PedidoTipoSerializer

class PedidoMensajeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoMensaje
        field = ('id','desc_mens')
        exclude = ['created','updated','esta_ttus','codi_tipe','pred_mens']

class PedidoMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoMensaje
        field = ('id','deleted')
        exclude =['created','updated','esta_ttus','desc_mens']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = str(instance.desc_mens).strip().upper()
        
        queryset = PedidoTipo.searchOrderTypeById(instance.codi_tipe.id)
        result_detail = PedidoTipoSerializer(queryset, many=True).data
        representation['type_order_all'] = result_detail
        return representation
    
    """
        Validate Description Pedido Mensaje
    """    
    def validate_desc_mens(value,state, _id:None):
        if _id is not None:
            queryset = PedidoMensaje.objects.filter(desc_mens = str(value).lower().strip()).exclude(id=_id) if state else PedidoMensaje.get_queryset().filter(desc_mens = str(value).lower().strip()).exclude(id=_id)
        else:
            queryset = PedidoMensaje.objects.filter(desc_mens = str(value).lower().strip()) if state else PedidoMensaje.get_queryset().filter(desc_mens = str(value).lower().strip())
        
        if queryset.count() == 0:
            return False
        else:
            return True
    
    """
    Validate Id Message Order

    Returns:
        _type_: True/False
    """
    def check_MessageOrder_Id(_id:None):
        resultSearchMessageOrder = False
        if _id is not None:
            queryset = PedidoMensaje.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                resultSearchMessageOrder = True
        
        return resultSearchMessageOrder
    
    """
        Validate Order Type Id
    """    
    def validate_OrderType(value):
        queryset = PedidoTipo.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    
class PedidoMensajeComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoMensaje
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','deleted','desc_mens','codi_tipe','pred_mens']

    def to_representation(self, instance):
        data = super(PedidoMensajeComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.desc_mens).upper()
        return data
    