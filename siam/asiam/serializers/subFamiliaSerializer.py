from datetime import datetime
from rest_framework import serializers
from asiam.models import SubFamilia

class SubFamiliaSerializer(serializers.ModelSerializer):
    familia = serializers.ReadOnlyField(source='codi_fami.desc_fami')

    class Meta:
        model = SubFamilia
        field = ('id','desc_sufa','abae_sufa','agru_sufa','codi_fami','familia')
        exclude =['created','updated','deleted','esta_ttus']
    