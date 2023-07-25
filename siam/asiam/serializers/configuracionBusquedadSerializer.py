from rest_framework import serializers
from asiam.models import ConfiguracionBusquedad

class ConfiguracionBusquedadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfiguracionBusquedad
        fields = ('id','nomb_camp','titu_camp','busc_camp','orde_camp','codi_tabl')
        read_only_fields = ('id', )