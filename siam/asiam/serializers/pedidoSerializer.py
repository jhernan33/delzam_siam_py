import os
from typing import List
from rest_framework import serializers
from asiam.models import Pedido,Cliente
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
        field = ('id',)
        exclude =['created','updated','esta_ttus','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi','codi_mone','codi_espe','codi_tipe']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = instance.codi_clie
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
        exclude = ['created','updated','esta_ttus','codi_clie','deleted']

    def to_representation(self, instance):
        data = super(PedidoComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = instance.codi_clie
        return data
    
class PedidoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        field = ('id','codi_clie')
        exclude = ['created','updated','esta_ttus']
