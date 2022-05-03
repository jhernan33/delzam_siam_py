from rest_framework import serializers
from asiam.models import Familia

class FamiliaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Familia
        fields = ('id','desc_fami','abae_fami','agru_fami','created','updated','deleted')
        # fields = ['id','desc_fami','agru_fami']
        # fields = "__all__"        
        read_only_fields = ('id', )