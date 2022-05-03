from rest_framework import serializers
from asiam.models import Iva

class IvaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Iva
        fields = ('id','alic_iva','fini_iva','ffin_iva')
        read_only_fields = ('id', )