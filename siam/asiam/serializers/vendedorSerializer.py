from dataclasses import field
from rest_framework import serializers
from asiam.serializers import NaturalSerializer
from asiam.models import Vendedor

class VendedorSerializer(serializers.ModelSerializer):
    codi_natu = NaturalSerializer()
    
    class Meta:
        model = Vendedor
        field = ('id','fein_vend','foto_vend','codi_natu')
        exclude =['created','updated','deleted','esta_ttus']