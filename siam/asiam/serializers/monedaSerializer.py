import os
from typing import List
from rest_framework import serializers
from asiam.models import Moneda
from django.conf import settings
from django.conf.urls.static import static
from asiam.serializers import PaisSerializer

class MonedaSerializer(serializers.ModelSerializer):
    # codi_pais = PaisSerializer()
    class Meta:
        model = Moneda
        field = ('id')
        exclude =['created','updated','esta_ttus','desc_mone','simb_mone','codi_mone']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = str(instance.desc_mone).upper()
        codi_pais = PaisSerializer(instance.codi_pais).data
        representation['country'] = codi_pais
        representation['symbol'] = instance.simb_mone
        representation['code'] = instance.codi_mone
        return representation
    
    """
        Validate Description Currency
    """    
    def validate_desc_mone(value,state, _id:None):
        if _id is not None:
            queryset = Moneda.objects.filter(desc_mone = str(value).lower().strip()) if state else Moneda.get_queryset().filter(desc_mone = str(value).lower().strip())
        else:
            queryset = Moneda.objects.filter(desc_mone = str(value).lower().strip()).filter(id) if state else Moneda.get_queryset().filter(desc_mone = str(value).lower().strip())
        
        if queryset.count() == 0:
            return False
        else:
            return True
    
    """
    Validate Id Currency

    Returns:
        _type_: True/False
    """
    def check_Currency_Id(_id:None):
        resultSearchCurrrency = False
        if _id is not None:
            queryset = Moneda.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                resultSearchCurrrency = True
        
        return resultSearchCurrrency

class MonedaComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','deleted','codi_pais','simb_mone','codi_mone','desc_mone']

    def to_representation(self, instance):
        data = super(MonedaComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.desc_mone).upper()
        return data
    
class MonedaBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        field = ('id','desc_mone')
        exclude = ['created','updated','esta_ttus','codi_pais','simb_mone','codi_mone']
