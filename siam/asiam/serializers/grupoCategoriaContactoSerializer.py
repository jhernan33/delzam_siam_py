
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import GrupoCategoriaContacto
from asiam.serializers import CategoriaContactoSerializer

class GrupoCategoriaContactoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoCategoriaContacto
        field = ('id','desc_grup')
        exclude = ['codi_ctco','deleted','created','updated','esta_ttus']


class GrupoCategoriaContactoSerializer(serializers.ModelSerializer):
    codi_ctco = CategoriaContactoSerializer()

    class Meta:
        model = GrupoCategoriaContacto
        field = ('id','desc_grup','codi_ctco','deleted')
        exclude =['created','updated','esta_ttus']
    
    
