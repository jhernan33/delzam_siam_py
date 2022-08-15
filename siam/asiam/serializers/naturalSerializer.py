from rest_framework import serializers
from asiam.serializers import CiudadSerializer, SectorSerializer
from asiam.models import Natural

class NaturalBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Natural
        field = ('id')
        exclude = ['naci_pena','cedu_pena','prno_pena','seno_pena','prap_pena','seap_pena','sexo_pena','fena_pena','dire_pena','riff_pena','codi_ciud'
        ,'deleted','created','updated','esta_ttus','edoc_pena','codi_sect']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        natural = Natural.get_queryset().filter(id=instance.id).values('prno_pena','seno_pena','prap_pena','seap_pena')
        
        representation['description'] = (natural[0]['prno_pena']+' '+natural[0]['seno_pena']+' '+natural[0]['prap_pena']+' '+natural[0]['seap_pena']).strip().upper()
        return representation

class NaturalSerializer(serializers.ModelSerializer):
    codi_ciud = CiudadSerializer()
    codi_sect = SectorSerializer()

    class Meta:
        model = Natural
        field = ['id','naci_pena','cedu_pena','prno_pena','seno_pena','prap_pena','seap_pena','sexo_pena','fena_pena'
        ,'dire_pena','riff_pena','nomb_apel','nombre_completo','apellido_completo','riff_pena','codi_ciud','deleted']
        exclude =['created','updated','esta_ttus']
    
    def to_representation(self, instance):
        data = super(NaturalSerializer, self).to_representation(instance=instance)
        data['naci_pena'] = data['naci_pena'].upper().strip() if data['naci_pena'] else data['naci_pena']
        data['prno_pena'] = data['prno_pena'].upper().strip() if data['prno_pena'] else data['prno_pena']
        data['seno_pena'] = data['seno_pena'].upper().strip() if data['seno_pena'] else data['seno_pena']
        data['prap_pena'] = data['prap_pena'].upper().strip() if data['prap_pena'] else data['prap_pena']
        data['seap_pena'] = data['seap_pena'].upper().strip() if data['seap_pena'] else data['seap_pena']
        data['sexo_pena'] = data['sexo_pena'].upper().strip() if data['sexo_pena'] else data['sexo_pena']
        data['dire_pena'] = data['dire_pena'].upper().strip() if data['dire_pena'] else data['dire_pena']
        data['riff_pena'] = data['riff_pena'].upper().strip() if data['riff_pena'] else data['riff_pena']
        data['nombre_completo'] = data['prno_pena'].upper().strip()+' '+data['seno_pena'].upper().strip() if data['prno_pena'].upper().strip() else data['prno_pena'].upper().strip()
        data['apellido_completo'] = data['prap_pena'].upper().strip()+' '+data['seap_pena'].upper().strip() if data['prap_pena'].upper().strip() else data['prap_pena'].upper().strip()
        return data
    
    def validate_cedu_pena(value):
        queryset = Natural.get_queryset().filter(cedu_pena = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    
    def validate_riff_pena(value,Dni):
        queryset = Natural.get_queryset().filter(riff_pena = value).exclude(cedu_pena=Dni)
        if queryset.count() == 0:
            return False
        else:
            return True