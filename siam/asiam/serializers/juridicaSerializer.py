from rest_framework import serializers
from asiam.serializers import TipoEmpresaSerializer
from asiam.models import Juridica

class JuridicaSerializer(serializers.ModelSerializer):
    codi_tiem = TipoEmpresaSerializer()
        
    class Meta:
        model = Juridica
        fields = ('id','riff_peju','raso_peju','dofi_peju','ivaa_peju','islr_peju','desc_peju','codi_tiem')
        read_only_fields = ('id', )