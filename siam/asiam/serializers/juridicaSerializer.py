import os
from django.conf import settings

from rest_framework import serializers
from asiam.serializers import TipoEmpresaSerializer, CiudadSerializer, SectorSerializer
from asiam.models import Juridica

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentSeller = os.path.realpath(settings.WEBSERVER_LEGAL)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentSeller+obj['image']
            return value

    def to_internal_value(self, data):
        return data

class JuridicaBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juridica
        field = ('id')
        exclude = ['riff_peju','raso_peju','dofi_peju','ivaa_peju','islr_peju','desc_peju','codi_tiem','deleted','created','updated','esta_ttus','fori_peju','folo_peju','pure_peju','fevi_peju','codi_ciud','codi_sect']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        juridica = Juridica.get_queryset().filter(id=instance.id).values('raso_peju')
        
        representation['description'] = juridica[0]['raso_peju'].strip().upper()
        return representation

class JuridicaSerializer(serializers.ModelSerializer):
    codi_tiem = TipoEmpresaSerializer()
    codi_ciud = CiudadSerializer()  
    codi_sect = SectorSerializer()
    fori_peju = JSONSerializerField()
    folo_peju = JSONSerializerField()
    
    class Meta:
        model = Juridica
        field = ['id','riff_peju','raso_peju','dofi_peju','ivaa_peju','islr_peju','desc_peju','codi_tiem','deleted']
        exclude =['created','updated','esta_ttus']
    
    def to_representation(self, instance):
        data = super(JuridicaSerializer, self).to_representation(instance=instance)
        data['raso_peju'] = data['raso_peju'].upper().strip() if data['raso_peju'] else data['raso_peju']
        data['riff_peju'] = data['riff_peju'].upper().strip() if data['riff_peju'] else data['riff_peju']
        data['dofi_peju'] = data['dofi_peju'].upper().strip() if data['dofi_peju'] else data['dofi_peju']
        data['desc_peju'] = data['desc_peju'].upper().strip() if data['desc_peju'] else data['desc_peju']
        data['pure_peju'] = data['pure_peju'].upper().strip() if data['pure_peju'] else data['pure_peju']
        return data
    
    def validate_riff_peju(value,Id):
        queryset = Juridica.get_queryset().filter(riff_peju = value).exclude(id = Id)
        if queryset.count() == 0:
            return False
        else:
            return True