from rest_framework import serializers
from asiam.models import Municipio

class MunicipioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Municipio
        fields = ('id','nomb_muni','codi_esta_id',)
        read_only_fields = ('id', 'codi_esta_id',)