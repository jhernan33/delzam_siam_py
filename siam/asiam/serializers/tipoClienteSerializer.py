from rest_framework import serializers
from asiam.models import Tipocliente

class TipoClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tipocliente
        fields = ('id','desc_ticl')
        read_only_fields = ('id','desc_ticl', )