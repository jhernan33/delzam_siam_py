from dataclasses import fields
from datetime import datetime
from rest_framework import serializers
from asiam.models import Ciudad
from asiam.serializers import EstadoSerializer

class CiudadSerializer(serializers.ModelSerializer):
    # estado = serializers.ReadOnlyField(source='codi_esta.nomb_esta')
    codi_esta = EstadoSerializer()

    class Meta:
        model = Ciudad
        field = ['id','nomb_ciud','codi_esta']
        exclude =['created','updated','deleted','esta_ttus']

    def to_representation(self, instance):
        data = super(CiudadSerializer, self).to_representation(instance=instance)
        data['nomb_ciud'] = data['nomb_ciud'].upper().strip() if data['nomb_ciud'] else data['nomb_ciud']
        # data['estado'] = data['estado'].upper().strip() if data['estado'] else data['estado']
        return data