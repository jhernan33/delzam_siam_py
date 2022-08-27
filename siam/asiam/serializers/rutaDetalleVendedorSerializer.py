from datetime import datetime
from rest_framework import serializers
from asiam.models import RutaDetalleVendedor
from asiam.serializers import VendedorSerializer


class RutaDetalleVendedorSerializerBasics(serializers.ModelSerializer):
    class Meta:
        model = RutaDetalleVendedor
        field = ('codi_vend')
        exclude =['created','updated','deleted','esta_ttus','id','codi_ruta']

class RutaDetalleVendedorSerializer(serializers.ModelSerializer):
    codi_vend = VendedorSerializer()
    # zona = serializers.PrimaryKeyRelatedField(queryset = Zona.get_queryset())
    # Vendedor = VendedorSerializer(many=True, read_only=True)

    class Meta:
        model = RutaDetalleVendedor
        field = ('id','codi_ruta')
        exclude =['created','updated','deleted','esta_ttus']
