from datetime import datetime
from rest_framework import serializers
from asiam.models import Estado
from asiam.serializers import PaisSerializer

class EstadoSerializer(serializers.ModelSerializer):
    codi_pais = PaisSerializer()
    
    class Meta:
        model = Estado
        field = ('id','codi_pais')
        exclude =['created','updated','deleted','esta_ttus']
