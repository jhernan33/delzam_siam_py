import os
from django.conf import settings

from rest_framework import serializers
from asiam.serializers import TipoEmpresaSerializer, CiudadSerializer, SectorSerializer
from asiam.models import Juridica, Contacto, CategoriaContacto

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

        """ Search Conctac by instance Id"""
        queryset = Contacto.objects.filter(codi_juri = instance.id)
        result_contact = ContactSimpleSerializer(queryset, many=True).data
        data['contacts'] = {"data":result_contact}

        return data
    
    def validate_riff_peju(value,Id):
        queryset = Juridica.get_queryset().filter(riff_peju = value).exclude(id = Id)
        if queryset.count() == 0:
            return False
        else:
            return True