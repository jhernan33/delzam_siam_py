from rest_framework import serializers
from asiam.models import TipoEmpresa

class TipoEmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoEmpresa
        fields = ('id','desc_tiem',)
        read_only_fields = ('id', )