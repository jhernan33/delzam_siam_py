from dataclasses import fields
from datetime import datetime
from rest_framework import serializers
from asiam.models import Ruta,Zona,RutaDetalleVendedor

# class TrackListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         return 'Detalle %d: ' % (value.codi_vend)

class RutaSerializer(serializers.ModelSerializer):
    
    # Ruta = serializers.SerializerMethodField()

    # def get_Ruta(self, obj):
    #     rutas = obj.Ruta.all()
    #     if not rutas:
    #         return None
    #     return RutaDetalleVendedor(rutas, many=True).data

    #Ruta = RutaDetalleVendedor(source='RutaDetalleVendedors', many=True)
    #ruta = TrackListingField(many=True, read_only=True)
    zona = serializers.ReadOnlyField(source='codi_zona.desc_zona')
    #vendedor = 
    # Ruta = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # vendedor = serializers.ReadOnlyField(source='codi_vend.codi_natu.prno_pena')
    # zona = serializers.PrimaryKeyRelatedField(queryset = Zona.get_queryset())

    class Meta:
        model = Ruta
        field = ('id','nomb_ruta','codi_zona','zona','vendedor')
        # fields = ['id','nomb_ruta','codi_zona','rutas']
        exclude =['created','updated','deleted','esta_ttus']

