from rest_framework import serializers
from asiam.models import Sector

class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        field = ('id','codi_ciud_id')
        exclude =['created','updated','deleted','esta_ttus']