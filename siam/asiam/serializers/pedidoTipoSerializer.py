import os
from typing import List
from rest_framework import serializers
from asiam.models import PedidoTipo
from django.conf import settings
from django.conf.urls.static import static

class PedidoTipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PedidoTipo
        field = ('id',)
        exclude =['created','updated','esta_ttus','desc_tipe','orde_tipe']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = str(instance.desc_tipe).upper()
        representation['ordering'] = instance.orde_tipe
        return representation
    
    def validate_desc_tipe(value,state, _id:None):
        if _id is not None:
            queryset = PedidoTipo.objects.filter(desc_tipe = str(value).lower().strip()) if state else PedidoTipo.get_queryset().filter(desc_tipe = str(value).lower().strip())
        else:
            queryset = PedidoTipo.objects.filter(desc_tipe = str(value).lower().strip()).filter(id) if state else PedidoTipo.get_queryset().filter(desc_tipe = str(value).lower().strip())
        
        if queryset.count() == 0:
            return False
        else:
            return True
    
    '''
        Validate State Id 
    '''
    def validate_codi_tipe(value):
        queryset = PedidoTipo.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    

class PedidoTipoComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoTipo
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','orde_tipe','desc_tipe','deleted']

    def to_representation(self, instance):
        data = super(PedidoTipoComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.desc_tipe).upper()
        return data
    
class PedidoTipoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoTipo
        field = ('id','desc_tipe')
        exclude = ['created','updated','esta_ttus','orde_tipe']
