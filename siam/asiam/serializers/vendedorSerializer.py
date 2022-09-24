from dataclasses import field
from operator import truediv
import os

from django.conf import settings
from rest_framework import serializers
from django.db.models import Q
from asiam.serializers import NaturalSerializer
from asiam.models import Vendedor,Natural,RutaDetalleVendedor, Contacto, CategoriaContacto

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

class ContactSimpleSerializer(serializers.ModelSerializer):
    desc_grup = serializers.ReadOnlyField(source='codi_grco.desc_grup')
    codi_cate = serializers.ReadOnlyField(source='codi_grco.codi_ctco_id')
    
    class Meta:
        model = Contacto
        field = ('id','desc_grup','codi_cate')
        exclude = ['codi_clie','codi_prov','codi_vend','codi_natu','codi_juri','codi_acci','deleted','created','updated','esta_ttus']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['codi_cont'] = instance.desc_cont
        representation['codi_grou'] = instance.codi_grco_id
        result_category_contact = CategoriaContacto.objects.filter(id = instance.codi_grco.codi_ctco_id)
        representation['desc_cate'] = result_category_contact[0].desc_ctco 
        return representation


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
    foto_vend = JSONSerializerField()

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

        """ Search Conctac by instance Id"""
        queryset = Contacto.objects.filter(Q(codi_vend = instance.id) | Q(codi_natu = instance.codi_natu))
        result_contact = ContactSimpleSerializer(queryset, many=True).data
        data['contacts'] = {"data":result_contact}

        return data