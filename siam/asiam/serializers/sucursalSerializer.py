from rest_framework import serializers
from asiam.models import Sucursal

class SucursalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sucursal
        fields = ('id','dofi_sucu','desc_sucu','riff_peju','codi_muni','codi_sect','repr_sucu','folo_peju','pure_peju')
        read_only_fields = ('id','dofi_sucu', )