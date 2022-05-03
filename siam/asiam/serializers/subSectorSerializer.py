from rest_framework import serializers
from asiam.models import SubSector

class SubSectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubSector
        fields = ('id','nomb_suse','codi_sect_id',)
        read_only_fields = ('id','codi_sect_id',)