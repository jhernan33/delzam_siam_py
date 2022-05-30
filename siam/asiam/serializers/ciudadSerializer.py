from dataclasses import fields
from datetime import datetime
from rest_framework import serializers
from asiam.models import Ciudad
from asiam.serializers import EstadoSerializer

class CiudadSerializer(serializers.ModelSerializer):
    estado = serializers.ReadOnlyField(source='codi_esta.nomb_esta')
    
    class Meta:
        model = Ciudad
        field = ['id','nomb_ciud','codi_esta','estado']
        exclude =['created','updated','deleted','esta_ttus']
