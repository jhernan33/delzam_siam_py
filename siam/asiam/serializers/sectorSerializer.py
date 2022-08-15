from rest_framework import serializers
from asiam.models import Sector

class SectorBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        field = ('id','nomb_sect')
        exclude = ['codi_ciud','created','updated','deleted','esta_ttus']

class SectorSerializer(serializers.ModelSerializer):
    ciudad = serializers.ReadOnlyField(source='codi_ciud.nomb_ciud')

    class Meta:
        model = Sector
        field = ('id','codi_ciud','ciudad')
        exclude =['created','updated','deleted','esta_ttus']
    
    def to_representation(self, instance):
        data = super(SectorSerializer, self).to_representation(instance=instance)
        data['ciudad'] = data['ciudad'].upper().strip() if data['ciudad'] else data['ciudad']
        return data