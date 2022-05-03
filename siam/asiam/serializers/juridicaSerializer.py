from rest_framework import serializers
from asiam.models import Juridica

class JuridicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Juridica
        fields = ('id','riff_peju','raso_peju','dofi_peju','ivaa_peju','islr_peju','desc_peju','codi_tiem_id',)
        read_only_fields = ('id','codi_tiem_id', )