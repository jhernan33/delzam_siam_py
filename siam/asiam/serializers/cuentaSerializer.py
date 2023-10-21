from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import Banco, Cuenta
from asiam.serializers.bancoSerializer import BancoComboSerializer, BancoBasicSerializer, BancoSerializer


class CuentaBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        field = ('id','ncta_cuen')
        exclude = ['created','updated','esta_ttus','fape_cuen','tipo_cuen','codi_banc']

class CuentaSerializer(serializers.ModelSerializer):
    codi_banc = BancoSerializer()
    class Meta:
        model = Cuenta
        field = ('id','codi_banc','deleted')
        exclude =['created','updated','esta_ttus','ncta_cuen','fape_cuen','tipo_cuen']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['account_number'] = str(instance.ncta_cuen).upper()
        representation['opening_date'] = instance.fape_cuen
        representation['type'] = instance.tipo_cuen
        return representation
    
    """
        Validate Bank Account number of Bank
    """    
    def validate_ncta_cuen(_account,_bank,state, _id:None):
        queryset = []
        
        # Instance of Bank
        _bank = Banco.get_queryset().get(id = _bank)
        # Check Id Bank Account
        if _id is not None:
            queryset = Cuenta.objects.filter(ncta_cuen = str(_account).lower().strip()).filter(codi_banc = _bank).exclude(id=_id) if state else Cuenta.get_queryset().filter(ncta_cuen = str(_account).lower().strip()).filter(codi_banc = _bank).exclude(id=_id)
        else:
            queryset = Cuenta.objects.filter(ncta_cuen = str(_account).lower().strip()).filter(codi_banc = _bank) if state else Cuenta.get_queryset().filter(ncta_cuen = str(_account).lower().strip()).filter(codi_banc = _bank)
        
        if queryset.count() == 0:
            return False
        else:
            return True
    
    """
    Validate Id Bank

    Returns:
        _type_: True/False
    """
    def check_Account_Id(_id:None):
        resultSearchBank = False
        if _id is not None:
            queryset = Cuenta.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                resultSearchBank = True
        
        return resultSearchBank
    
class CuentaComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','deleted','fape_cuen','tipo_cuen','codi_banc','ncta_cuen']

    def to_representation(self, instance):
        data = super(CuentaComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.ncta_cuen).upper()
        return data
    