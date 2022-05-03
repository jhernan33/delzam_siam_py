from rest_framework import serializers
from asiam.models import sector

class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = sector
        fields = ('id','nomb_sect','codi_ciud_id',)
        read_only_fields = ('id','codi_ciud_id', )