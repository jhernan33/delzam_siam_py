import os
from typing import List
from rest_framework import serializers
from asiam.models import PedidoEstatus
from django.conf import settings
from django.conf.urls.static import static

class PedidoEstatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = PedidoEstatus
        field = ('id',)
        exclude =['created','updated','esta_ttus','desc_esta','orde_esta']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = str(instance.desc_esta).upper()
        representation['ordering'] = instance.orde_esta
        return representation
    
    def validate_desc_esta(value,state, _id:None):
        if _id is not None:
            queryset = PedidoEstatus.objects.filter(desc_esta = str(value).lower().strip()) if state else PedidoEstatus.get_queryset().filter(desc_esta = str(value).lower().strip())
        else:
            queryset = PedidoEstatus.objects.filter(desc_esta = str(value).lower().strip()).filter(id) if state else PedidoEstatus.get_queryset().filter(desc_esta = str(value).lower().strip())
        
        if queryset.count() == 0:
            return False
        else:
            return True
    

class PedidoEstatusComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoEstatus
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','orde_esta','desc_esta','deleted']

    def to_representation(self, instance):
        data = super(PedidoEstatusComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.desc_esta).upper()
        return data
    
class PedidoEstatusBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoEstatus
        field = ('id','desc_esta')
        exclude = ['created','updated','esta_ttus','orde_esta']
