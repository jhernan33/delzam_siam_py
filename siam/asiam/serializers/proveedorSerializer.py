import os
from typing import List
from rest_framework import serializers
from asiam.serializers import NaturalSerializer,JuridicaSerializer
from asiam.models import Proveedor,Natural, Juridica
from django.conf import settings
from django.conf.urls.static import static

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentArticle = os.path.realpath(settings.WEBSERVER_SUPPLIER)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentArticle+obj['image'];
            return value

    def to_internal_value(self, data):
        return data

class ProveedorBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        field = ('id')
        exclude =['created','updated','esta_ttus','codi_repr','mocr_prov','plcr_prov','foto_prov','obse_prov','deleted','codi_natu','codi_juri']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        natural = Natural.get_queryset().filter(id=instance['codi_natu_id']).values('prno_pena','seno_pena','prap_pena','seap_pena')
        juridica = Juridica.get_queryset().filter(id=instance['codi_juri_id']).values('raso_peju')
        
        representation['natural'] = (natural[0]['prno_pena']+' '+natural[0]['seno_pena']+' '+natural[0]['prap_pena']+' '+natural[0]['seap_pena']).upper()
        representation['juridico'] = (juridica[0]['raso_peju']).upper()
        return representation

class ProveedorSerializer(serializers.ModelSerializer):
    codi_natu = NaturalSerializer()
    codi_juri = JuridicaSerializer()
    codi_repr = NaturalSerializer()
    foto_prov = JSONSerializerField()

    class Meta:
        model = Proveedor
        field = ('id','codi_natu','codi_juri','codi_repr','mocr_prov','plcr_prov','foto_prov','obse_prov','deleted')
        exclude =['created','updated','esta_ttus']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        natural = Natural.get_queryset().filter(id=instance.codi_natu_id).values('prno_pena','seno_pena','prap_pena','seap_pena')
        juridica = Juridica.get_queryset().filter(id=instance.codi_juri_id).values('raso_peju')
        
        representation['description_natural'] = (natural[0]['prno_pena']+' '+natural[0]['seno_pena']+' '+natural[0]['prap_pena']+' '+natural[0]['seap_pena']).upper().strip()
        representation['description_juridico'] = (juridica[0]['raso_peju']).upper().strip()
        return representation

    def validate_codi_natu(value):
        queryset = Natural.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    
    def validate_codi_juri(value):
        queryset = Juridica.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    
    
