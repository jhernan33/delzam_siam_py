from rest_framework import serializers
from asiam.models import IvaGeneral

class IvaGeneralSerializer(serializers.ModelSerializer):

    class Meta:
        model = IvaGeneral
        field = ('id','desc_ivag')
        exclude =['created','updated','deleted','esta_ttus']