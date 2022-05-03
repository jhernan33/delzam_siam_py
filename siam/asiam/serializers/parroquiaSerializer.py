from rest_framework import serializers
from asiam.models import Parroquia

class ParroquiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parroquia
        fields = ('id','nomb_parr','codi_muni_id',)
        read_only_fields = ('id','codi_muni_id',)