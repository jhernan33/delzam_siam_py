from rest_framework import serializers
from asiam.serializers import TipoEmpresaSerializer, CiudadSerializer, SectorSerializer
from asiam.models import Juridica

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