from datetime import datetime
from rest_framework import serializers
from asiam.models import RutaDetalleVendedor
from asiam.serializers import VendedorSerializer

class RutaDetalleVendedorSerializer(serializers.ModelSerializer):
    codi_vend = VendedorSerializer()
    # zona = serializers.PrimaryKeyRelatedField(queryset = Zona.get_queryset())
    # Vendedor = VendedorSerializer(many=True, read_only=True)

    class Meta:
        model = RutaDetalleVendedor
        field = ('id','codi_ruta','codi_vend')
        exclude =['created','updated','deleted','esta_ttus']
