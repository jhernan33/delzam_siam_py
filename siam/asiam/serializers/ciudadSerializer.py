from dataclasses import fields
from datetime import datetime
from rest_framework import serializers
from asiam.models import Ciudad
from asiam.serializers import EstadoSerializer

class CiudadBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        field = ('id','nomb_ciud')
        exclude = ['codi_esta','created','updated','deleted','esta_ttus']

class CiudadSerializer(serializers.ModelSerializer):
    codi_esta = EstadoSerializer()

    class Meta:
        model = Ciudad
        field = ['id','nomb_ciud','codi_esta','deleted']
        exclude =['created','updated','esta_ttus']

    def to_representation(self, instance):
        data = super(CiudadSerializer, self).to_representation(instance=instance)
        data['nomb_ciud'] = data['nomb_ciud'].upper().strip() if data['nomb_ciud'] else data['nomb_ciud']
        return data
    
    def validate_nomb_ciud(value,id):
        queryset = Ciudad.get_queryset().filter(nomb_ciud = value).exclude(id=id)
        if queryset.count() == 0:
            return False
        else:
            return True

    def validate_codi_cuid(value):
        queryset = Ciudad.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True