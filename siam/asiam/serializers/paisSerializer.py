from rest_framework import serializers
from asiam.models import pais

class PaisSerializer(serializers.ModelSerializer):

    class Meta:
        model = pais
        fields = ('id','nomb_pais',)
        read_only_fields = ('id', )