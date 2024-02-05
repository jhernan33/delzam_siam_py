from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import Banco, Cuenta
from asiam.serializers.rutaDetalleVendedorSerializer import RutaDetalleVendedorSerializer, RutaDetalleVendedorSerializerBasics
from asiam.serializers.clienteSerializer import ClienteBasicSerializer, ClienteRutaSerializer

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentBank = os.path.realpath(settings.WEBSERVER_BANK)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentBank+obj['image']
            return value

    def to_internal_value(self, data):
        return data

class BancoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        field = ('id','desc_banc')
        exclude = ['created','updated','esta_ttus','logo_banc']

class BancoSerializer(serializers.ModelSerializer):
    logo_banc = JSONSerializerField()
    class Meta:
        model = Banco
        field = ('id','logo_banc','deleted')
        exclude =['created','updated','esta_ttus','desc_banc']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = str(instance.desc_banc).strip().upper()
        from asiam.serializers.cuentaSerializer import CuentaBasicSerializer

        # Search Account of Bank
        querysetAccountOfBank = Cuenta.filterByBankId(instance.id)
        resultAccountOfBank = CuentaBasicSerializer(querysetAccountOfBank, many=True).data
        representation['account_number'] = {"data":resultAccountOfBank}
        return representation
    
    """
        Validate Description Bank
    """    
    def validate_desc_banc(value,state, _id:None):
        if _id is not None:
            queryset = Banco.objects.filter(desc_banc = str(value).lower().strip()).exclude(id=_id) if state else Banco.get_queryset().filter(desc_banc = str(value).lower().strip()).exclude(id=_id)
        else:
            queryset = Banco.objects.filter(desc_banc = str(value).lower().strip()) if state else Banco.get_queryset().filter(desc_banc = str(value).lower().strip())
        
        if queryset.count() == 0:
            return False
        else:
            return True
    
    """
    Validate Id Bank

    Returns:
        _type_: True/False
    """
    def check_Bank_Id(_id:None):
        resultSearchBank = False
        if _id is not None:
            queryset = Banco.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                resultSearchBank = True
        
        return resultSearchBank
    
class BancoComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','deleted','desc_banc','logo_banc']

    def to_representation(self, instance):
        data = super(BancoComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.desc_banc).upper()
        return data
    