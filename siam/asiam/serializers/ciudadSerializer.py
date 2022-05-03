from rest_framework import serializers
from asiam.models import ciudad

class CiudadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ciudad
        read_only_fields = ('id','codi_esta','nomb_ciud')
        exclude =['created','updated','deleted']
