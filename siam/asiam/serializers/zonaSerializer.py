from rest_framework import serializers
from asiam.models import Zona

class ZonaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zona
        field = ('id','desc_zona')
        exclude =['created','updated','deleted','esta_ttus']