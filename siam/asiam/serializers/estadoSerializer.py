from datetime import datetime
from rest_framework import serializers
from asiam.models import Estado
from asiam.serializers import PaisSerializer

class EstadoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        field = ('id','nomb_esta')
        exclude = ['codi_pais','created','updated','deleted','esta_ttus']

class EstadoSerializer(serializers.ModelSerializer):
    codi_pais = PaisSerializer()
    
    class Meta:
        model = Estado
        field = ('id','codi_pais')
        exclude =['created','updated','deleted','esta_ttus']
    
    def validate_codi_esta(value):
        queryset = Estado.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True
