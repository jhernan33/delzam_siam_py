
from rest_framework.response import Response
from rest_framework import serializers
# from django.http import JsonResponse

from asiam.models import Ruta,RutaDetalleVendedor,Cliente
from asiam.serializers.rutaDetalleVendedorSerializer import RutaDetalleVendedorSerializer, RutaDetalleVendedorSerializerBasics
from asiam.serializers.clienteSerializer import ClienteBasicSerializer

# class TrackListingField(serializers.RelatedField):
#     def to_representation(self, value):
#         return 'Detalle %d: ' % (value.codi_vend)

class RutaBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        field = ('id')
        exclude = ['nomb_ruta','codi_zona','deleted','created','updated','esta_ttus']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        route = Ruta.objects.filter(id=instance.id).values('nomb_ruta')
        
        representation['description'] = (route[0]['nomb_ruta']).strip().upper()
        return representation

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
        
# Serialize Customer
class RutaClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        field = ('id','nomb_ruta')
        exclude =['created','updated','esta_ttus','deleted','posi_ruta','codi_zona']
    
    def to_representation(self, instance):
        data = super(RutaClienteSerializer, self).to_representation(instance=instance)

        queryset = RutaDetalleVendedor.objects.filter(codi_ruta=instance.id)
        customer = Cliente.objects.filter(ruta_detalle_vendedor_cliente__in=queryset)
        result = ClienteBasicSerializer(customer, many=True).data
        data['customers'] = result
        return data