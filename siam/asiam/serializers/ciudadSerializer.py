from rest_framework import serializers
from asiam.models import Ciudad

class CiudadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ciudad
        read_only_fields = ('id','codi_esta','nomb_ciud')
        exclude =['created','updated','deleted']
