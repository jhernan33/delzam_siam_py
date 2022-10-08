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
                obj['image'] = place+enviromentArticle+obj['image']
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
        naturalDescription = None
        juridicaDescription = None

        result_natural = '' if instance.codi_natu_id is None else Natural.objects.filter(id=instance.codi_natu_id).values('prno_pena','seno_pena','prap_pena','seap_pena')
        if result_natural.count()>0:
            naturalDescription = str(result_natural[0]['prno_pena']+' '+result_natural[0]['seno_pena']+' '+result_natural[0]['prap_pena']+' '+result_natural[0]['seap_pena']).upper().strip()

        representation['description_natural'] = naturalDescription
        
        if instance.codi_juri_id:
            juridica = Juridica.objects.filter(id=instance.codi_juri_id).values('raso_peju')     
            juridicaDescription = '' if juridica.count() < 1 else str(juridica[0]['raso_peju']).upper().strip()

        representation['description_juridico'] = juridicaDescription
        return representation

    def validate_codi_natu(value,state):
        queryset =  Natural.objects.filter(id = value) if state else Natural.get_queryset().filter(id = value)
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
    
    
