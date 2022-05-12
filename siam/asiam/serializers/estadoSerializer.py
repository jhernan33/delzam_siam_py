from rest_framework import serializers
from asiam.models import Estado

class EstadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estado
        # fields = ('id','nomb_esta','codi_pais')
        # fields = "__all__"
        read_only_fields = ('id','codi_pais')
        exclude =['created','updated','deleted','esta_ttus']
