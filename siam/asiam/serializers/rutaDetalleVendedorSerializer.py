from datetime import datetime
from rest_framework import serializers
from asiam.models import Ruta,Zona, RutaDetalleVendedor
from asiam.serializers import VendedorSerializer

class RutaDetalleVendedorSerializer(serializers.ModelSerializer):
    # vendedor = VendedorSerializer
    # zona = serializers.PrimaryKeyRelatedField(queryset = Zona.get_queryset())

    class Meta:
        model = RutaDetalleVendedor
        field = ('id','codi_ruta','codi_vend')
        exclude =['created','updated','deleted','esta_ttus']

