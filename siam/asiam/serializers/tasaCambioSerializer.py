from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import Banco, Cuenta, TasaCambio, Moneda
from asiam.serializers.monedaSerializer import MonedaSerializer

class TasaCambioBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasaCambio
        field = ('id','valo_taca')
        exclude = ['created','updated','esta_ttus','codi_mone','fech_taca','valo_taca','obse_taca','tipo_taca','codi_mone_to','codi_mone_to']

class TasaCambioSerializer(serializers.ModelSerializer):
    codi_mone = MonedaSerializer()
    codi_mone_to = MonedaSerializer()

    # obse_taca = serializers.CharField(max_length=254)
    # type = serializers.CharField(max_length=20)
    
    class Meta:
        model = TasaCambio
        field = ('id','codi_mone','codi_mone_to')
        exclude =['created','updated','esta_ttus','deleted','fech_taca','valo_taca','obse_taca','tipo_taca']
    


    def validateData(data):
        """
        Check currency From
        """
        if Moneda.checkCurrency( data['currency'] ) == False:
            raise serializers.ValidationError({'message':"Moneda no permitida"})

        if Moneda.checkCurrency( data['currencyTo'] ) == False:
            raise serializers.ValidationError({'message':"Moneda no permitida"})
        
        return True

    


    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.fech_taca
        representation['value'] = instance.valo_taca
        representation['observations'] = str(instance.obse_taca).strip()
        representation['type'] = str(instance.tipo_taca).strip().lower()
        return representation
    
    """
        Validate Exchange Rate
    """    
    def validate_exchange_rate(_currency,_date,state, _id:None):
        queryset = []
        
        # Instance of currency
        _currency = Moneda.get_queryset().get(id = _currency)
        # Check Id Tasa
        if _id is not None:
            queryset = TasaCambio.objects.exclude(id=_id) if state else TasaCambio.get_queryset().exclude(id=_id)
        else:
            queryset = TasaCambio.objects if state else TasaCambio.get_queryset()
        
        if queryset.count() == 0:
            return False
        else:
            return True
    
    """
    Validate Id Bank

    Returns:
        _type_: True/False
    """
    def check_Exchange_Rate_Id(_id:None):
        resultSearcExchangeRate = False
        if _id is not None:
            queryset = TasaCambio.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                resultSearcExchangeRate = True
        
        return resultSearcExchangeRate
    
class TasaCambioComboSerializer(serializers.ModelSerializer):
    currency = serializers.ReadOnlyField(source='codi_mone.desc_mone')
    # familyDescription = serializers.ReadOnlyField(source='codi_sufa.codi_fami.desc_fami')
    class Meta:
        model = TasaCambio
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','deleted','fech_taca','valo_taca','obse_taca','codi_mone','tipo_taca','codi_mone_to']

    def to_representation(self, instance):
        data = super(TasaCambioComboSerializer, self).to_representation(instance=instance)
        
        # Description
        data["description"] = str(instance.valo_taca).upper()
        return data
    