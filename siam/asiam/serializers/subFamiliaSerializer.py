from rest_framework import serializers
from asiam.models import SubFamilia

class SubFamiliaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubFamilia
        fields = ('id','desc_sufa','abae_sufa','agru_sufa','codi_fami')
        # fields = ['id','desc_fami','agru_fami']
        # fields = "__all__"        
        read_only_fields = ('id', )