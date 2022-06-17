from datetime import datetime
from rest_framework import serializers
from asiam.models import Presentacion

class PresentacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentacion
        field = ('id','desc_pres','tipo_pres','abre_pres')
        exclude =['created','updated','deleted','esta_ttus']


    