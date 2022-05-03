from rest_framework import serializers
from asiam.models import Zona

class ZonaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zona
        fields = ('id','desc_zona')
        read_only_fields = ('id', )