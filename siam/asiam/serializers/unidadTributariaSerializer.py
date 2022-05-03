from rest_framework import serializers
from asiam.models import UnidadTributaria

class UnidadTributariaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnidadTributaria
        fields = ('id','mont_untr','fini_untr','ffin_untr',)
        read_only_fields = ('id', )