
from rest_framework.response import Response
from rest_framework import serializers
# from django.http import JsonResponse

from asiam.models import Ruta,RutaDetalleVendedor
from asiam.serializers.rutaDetalleVendedorSerializer import RutaDetalleVendedorSerializer, RutaDetalleVendedorSerializerBasics

# class TrackListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         return 'Detalle %d: ' % (value.codi_vend)

class RutaSerializer(serializers.ModelSerializer):
    # Ruta = serializers.SerializerMethodField()
    #codi_vend = RutaDetalleVendedorSerializer(many=True)

    # def get_Ruta(self, obj):
    #     rutas = obj.Ruta.all()
    #     if not rutas:
    #         return None
    #     return RutaDetalleVendedor(rutas, many=True).data

    #Ruta = RutaDetalleVendedor(source='RutaDetalleVendedors', many=True)
    #ruta = TrackListingField(many=True, read_only=True)
    zona = serializers.ReadOnlyField(source='codi_zona.desc_zona')
    Ruta = RutaDetalleVendedorSerializer(many=True, read_only=True)
    #Ruta = serializers.StringRelatedField(many=True)

    # Ruta = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # vendedor = serializers.ReadOnlyField(source='codi_vend.codi_natu.prno_pena')
    # zona = serializers.PrimaryKeyRelatedField(queryset = Zona.get_queryset())
    class Meta:
        model = Ruta
        field = ('id','nomb_ruta','codi_zona','zona','Ruta','deleted')
        exclude =['created','updated','esta_ttus']
    
    def to_representation(self, instance):
        data = super(RutaSerializer, self).to_representation(instance=instance)
        data['nomb_ruta'] = data['nomb_ruta'].upper().strip() if data['nomb_ruta'] else data['nomb_ruta']
        data['zona'] = data['zona'].upper().strip() if data['zona'] else data['zona']
        data['seller_count'] = RutaDetalleVendedor.objects.all().filter(codi_ruta=instance.id).count()

        queryset = RutaDetalleVendedor.objects.filter(codi_ruta=instance.id)
        result = RutaDetalleVendedorSerializerBasics(queryset, many=True).data
        data['sellers'] = {"data":result}
        return data
    
