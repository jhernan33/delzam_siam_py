import datetime
from rest_framework import serializers
from asiam.models import Juridicaa

class JuridicaaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Juridicaa
        fields = ('id','codi_peju_id','codi_pena_id',)
        read_only_fields = ('id', )
