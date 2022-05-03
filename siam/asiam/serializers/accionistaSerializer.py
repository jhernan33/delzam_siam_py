from rest_framework import serializers
from asiam.models import Accionista

class AccionistaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accionista
        fields = ('id','codi_acci','codi_juri','fere_acci')
        read_only_fields = ('id','codi_acci', )