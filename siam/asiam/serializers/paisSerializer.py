import datetime
from rest_framework import serializers
from asiam.models import Pais

class PaisBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        field = ('id','nomb_pais')
        exclude = ['name_pais','dial_pais','code_pais','deleted','created','updated','esta_ttus']

class PaisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pais
        field = ('id','nomb_pais','name_pais','dial_pais','code_pais','deleted')
        exclude =['created','updated','esta_ttus']
    
