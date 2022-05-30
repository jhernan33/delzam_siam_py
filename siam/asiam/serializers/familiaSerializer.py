from datetime import datetime
from rest_framework import serializers
from asiam.models import Familia

class FamiliaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Familia
        field = ('id','desc_fami','abae_fami','agru_fami')
        exclude =['created','updated','deleted','esta_ttus']


    