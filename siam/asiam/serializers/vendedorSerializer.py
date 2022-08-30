from dataclasses import field
import os

from django.conf import settings
from rest_framework import serializers
from asiam.serializers import NaturalSerializer
from asiam.models import Vendedor,Natural,RutaDetalleVendedor

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentSeller = os.path.realpath(settings.WEBSERVER_SELLER)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentSeller+obj['image']
            return value

    def to_internal_value(self, data):
        return data
        
class VendedorBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        field = ('id')
        exclude =['created','updated','esta_ttus','fein_vend','foto_vend','codi_natu','deleted']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        natural = Natural.get_queryset().filter(id=instance.codi_natu_id).values('prno_pena','seno_pena','prap_pena','seap_pena')
        if natural.count() >0:
            representation['seller'] = (natural[0]['prno_pena']+' '+natural[0]['seno_pena']+' '+natural[0]['prap_pena']+' '+natural[0]['seap_pena']).upper()
        return representation

class VendedorSerializer(serializers.ModelSerializer):
    codi_natu = NaturalSerializer()
    
    class Meta:
        model = Vendedor
        field = ('id','fein_vend','foto_vend','codi_natu','deleted')
        exclude =['created','updated','esta_ttus']
    
    def to_representation(self, instance):
        data = super(VendedorSerializer, self).to_representation(instance=instance)
        # data['nomb_ruta'] = data['nomb_ruta'].upper().strip() if data['nomb_ruta'] else data['nomb_ruta']
        # data['zona'] = data['zona'].upper().strip() if data['zona'] else data['zona']
        data['route_count'] = RutaDetalleVendedor.objects.all().filter(codi_vend=instance.id).count()

        # queryset = RutaDetalleVendedor.objects.filter(codi_ruta=instance.id)
        # result = RutaDetalleVendedorSerializerBasics(queryset, many=True).data
        # data['sellers'] = {"data":result}
        return data
    
