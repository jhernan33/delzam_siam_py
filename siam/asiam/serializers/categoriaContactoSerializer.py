
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import CategoriaContacto
from asiam.serializers.rutaDetalleVendedorSerializer import RutaDetalleVendedorSerializer, RutaDetalleVendedorSerializerBasics

class CategoriaContactoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaContacto
        field = ('id','desc_ctco')
        exclude = ['deleted','created','updated','esta_ttus']


class CategoriaContactoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoriaContacto
        field = ('id','desc_ctco','deleted')
        exclude =['created','updated','esta_ttus']
    
    
