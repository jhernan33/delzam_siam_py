from rest_framework import serializers
from asiam.models import Sector
from asiam.serializers import CiudadSerializer, EstadoSerializer

class SectorBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        field = ('id','nomb_sect')
        exclude = ['codi_ciud','created','updated','deleted','esta_ttus']

class SectorSerializer(serializers.ModelSerializer):
    codi_ciud = CiudadSerializer()

    class Meta:
        model = Sector
        field = ('id','nomb_sect','codi_ciud','deleted')
        exclude =['created','updated','esta_ttus']
    
    def validate_nomb_sect(value,id):
        queryset = Sector.get_queryset().filter(nomb_sect = value).exclude(id=id)
        if queryset.count() == 0:
            return False
        else:
            return True