import os
from typing import List
from rest_framework import serializers
from asiam.models import Cliente, Vendedor, Natural, Juridica
from asiam.serializers import NaturalSerializer,JuridicaSerializer,VendedorSerializer
from django.conf import settings
from django.conf.urls.static import static


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
    codi_vend = VendedorSerializer()
    codi_natu = NaturalSerializer()
    codi_juri = JuridicaSerializer()

    class Meta:
        model = Cliente
        field = ('id','fein_clie','codi_ante','cred_clie','mocr_clie','plzr_clie'
        ,'prde_clie','prau_clie','codi_vend','codi_natu','codi_juri','foto_clie','obse_clie','deleted')
        exclude =['created','updated','esta_ttus']
    
    def validate_codi_vend(value):
        queryset = Vendedor.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True

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