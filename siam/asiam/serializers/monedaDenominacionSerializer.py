import os
from typing import List
from rest_framework import serializers
from asiam.models import MonedaDenominacion, Moneda
from django.conf import settings
from django.conf.urls.static import static
from asiam.serializers import MonedaSerializer

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentSeller = os.path.realpath(settings.WEBSERVER_CURRENCY)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentSeller+obj['image']
            return value

    def to_internal_value(self, data):
        return data

class MonedaDenominacionSerializer(serializers.ModelSerializer):
    foto_deno = JSONSerializerField()
    class Meta:
        model = MonedaDenominacion
        field = ('id','foto_deno','deleted')
        exclude =['created','updated','esta_ttus','nomb_deno','valo_deno','codi_mone','orde_deno','tipo_deno']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = str(instance.nomb_deno).upper()
        codi_mone = MonedaSerializer(instance.codi_mone).data
        representation['currency'] = codi_mone
        representation['currency_amount'] = instance.valo_deno
        representation['type'] = instance.tipo_deno
        representation['photo'] = instance.foto_deno
        representation['order'] = instance.orde_deno
        return representation
    
    """
        Validate Description Currency
    """    
    def validate_nomb_deno(value,state, _id:None):
        if _id is not None:
            queryset = MonedaDenominacion.objects.filter(nomb_deno = str(value).lower().strip()).exclude(id = _id) if state else MonedaDenominacion.get_queryset().filter(nomb_deno = str(value).lower().strip()).exclude(id = _id)
        else:
            queryset = MonedaDenominacion.objects.filter(nomb_deno = str(value).lower().strip()) if state else MonedaDenominacion.get_queryset().filter(nomb_deno = str(value).lower().strip())
        
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

class MonedaDenominacionComboSerializer(serializers.ModelSerializer):
    # foto_deno = JSONSerializerField()
    class Meta:
        model = MonedaDenominacion
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','deleted','nomb_deno','valo_deno','codi_mone','foto_deno','orde_deno','tipo_deno']

    def to_representation(self, instance):
        data = super(MonedaDenominacionComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.nomb_deno).upper()
        # data['logo'] = instance.foto_deno
        return data
    
class MonedaDenominacionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonedaDenominacion
        field = ('id','nomb_deno')
        exclude =['created','updated','esta_ttus','valo_deno','codi_mone','foto_deno','orde_deno','tipo_deno']

