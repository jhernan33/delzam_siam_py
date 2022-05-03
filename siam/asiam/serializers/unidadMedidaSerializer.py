from rest_framework import serializers
from asiam.models import UnidadMedida

class UnidadMedidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnidadMedida
        fields = ('id','desc_unme')
        read_only_fields = ('id', )