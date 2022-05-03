from rest_framework import serializers
from asiam.models import Ruta

class RutaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ruta
        fields = ('id','nomb_ruta','codi_zona','codi_vend')
        read_only_fields = ('id', )