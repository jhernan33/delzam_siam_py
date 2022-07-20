import os
from typing import List
from rest_framework import serializers
from asiam.serializers import NaturalSerializer,JuridicaSerializer
from asiam.models import Proveedor
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

class ProveedorSerializer(serializers.ModelSerializer):
    codi_natu = NaturalSerializer()
    codi_juri = JuridicaSerializer()
    representante = serializers.ReadOnlyField(source='codi_repr.codi_natu')
    foto_prov = JSONSerializerField()
    
    class Meta:
        model = Proveedor
        field = ('id','codi_natu','codi_juri','codi_repr','mocr_prov','plcr_prov','foto_prov','obse_prov')
        exclude =['created','updated','deleted','esta_ttus']
    
