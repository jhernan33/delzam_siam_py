from rest_framework import serializers
from asiam.models import Sector

class SectorSerializer(serializers.ModelSerializer):
    ciudad = serializers.ReadOnlyField(source='codi_ciud.nomb_ciud')

    class Meta:
        model = Sector
        field = ('id','codi_ciud','ciudad')
        exclude =['created','updated','deleted','esta_ttus']