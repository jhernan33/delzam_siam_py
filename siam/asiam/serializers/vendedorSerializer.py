from rest_framework import serializers
from asiam.models import Vendedor

class VendedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendedor
        fields = ('id','fein_vend','foto_vend','codi_natu')
        read_only_fields = ('id', )