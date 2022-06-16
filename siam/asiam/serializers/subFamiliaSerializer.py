from dataclasses import fields
from datetime import datetime
from pyexpat import model
from rest_framework import serializers
from asiam.models import SubFamilia

class SubFamiliaSerializer(serializers.ModelSerializer):
    familia = serializers.ReadOnlyField(source='codi_fami.desc_fami')
    # desc_sufa = serializers.CharField(trim_whitespace=False)

    class Meta:
        model = SubFamilia
        field = ('id','desc_sufa','abae_sufa','agru_sufa','codi_fami','familia')
        exclude =['created','updated','deleted','esta_ttus']
        extra_kwargs = {"desc_sufa": {"trim_whitespace" : False}}
    
    