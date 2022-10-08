from datetime import datetime
from numpy import result_type
from rest_framework import serializers
from asiam.models import RutaDetalleVendedor, Ruta
from asiam.serializers import VendedorSerializer, ZonaSerializer

class RouteSerializer(serializers.ModelSerializer):
    codi_zona = ZonaSerializer()
    class Meta:
        model = Ruta
        field = ('id','nomb_ruta','codi_zona','zona','Ruta','deleted')
        exclude =['created','updated','esta_ttus']

class RutaDetalleVendedorSerializerBasics(serializers.ModelSerializer):
    class Meta:
        model = RutaDetalleVendedor
        field = ('codi_vend')
        exclude =['created','updated','deleted','esta_ttus','id','codi_ruta']

class RutaDetalleVendedorSerializer(serializers.ModelSerializer):
    codi_vend = VendedorSerializer()
    codi_ruta = RouteSerializer()
    #codi_ruta = RutaDetalleVendedor()
    # zona = serializers.PrimaryKeyRelatedField(queryset = Zona.get_queryset())
    # Vendedor = VendedorSerializer(many=True, read_only=True)

    class Meta:
        model = RutaDetalleVendedor
        field = ('id','codi_vend','codi_ruta')
        exclude =['created','updated','deleted','esta_ttus']
