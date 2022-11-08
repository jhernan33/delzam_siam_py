import os
from typing import List
from rest_framework import serializers
from asiam.models import Cliente, Vendedor, Natural, Juridica, RutaDetalleVendedor
from asiam.serializers import NaturalSerializer,JuridicaSerializer,VendedorSerializer
from asiam.serializers.rutaDetalleVendedorSerializer import RutaDetalleVendedorSerializer
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_gis.serializers import GeoFeatureModelListSerializer


class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentArticle = os.path.realpath(settings.WEBSERVER_CUSTOMER)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentArticle+obj['image']
            return value

    def to_internal_value(self, data):
        return data

class ClienteSerializer(serializers.ModelSerializer):
#class ClienteSerializer(GeoFeatureModelListSerializer):
    # codi_vend = VendedorSerializer()
    ruta_detalle_vendedor_cliente = RutaDetalleVendedorSerializer()
    codi_natu = NaturalSerializer()
    codi_juri = JuridicaSerializer()
    foto_clie = JSONSerializerField()

    class Meta:
        model = Cliente
        field = ('id','fein_clie','codi_ante','cred_clie','mocr_clie','plcr_clie'
        ,'prde_clie','prau_clie','codi_natu','codi_juri','foto_clie','obse_clie','deleted','ruta_detalle_vendedor_cliente','ptor_clie')
        exclude =['created','updated','esta_ttus']
        geo_field = "location_clie"
        # auto_bbox = True # Ubckyd
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['codi_ante'] = str(instance.codi_ante).upper()
        return representation
    
    def validate_codi_vend(value):
        queryset = RutaDetalleVendedor.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True

    def validate_codi_natu(value,state):
        queryset = Natural.objects.filter(id = value) if state else Natural.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True    
    
    def validate_codi_juri(value,state):
        queryset = Juridica.objects.filter(id = value) if state else Juridica.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True

class ClienteBasicSerializer(serializers.ModelSerializer):
     class Meta:
        model = Cliente
        field = ('id','codi_natu')
        exclude = ['created','updated','esta_ttus','fein_clie','codi_ante','cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie','obse_clie','deleted','ruta_detalle_vendedor_cliente','ptor_clie','location_clie','codi_juri','posi_clie']