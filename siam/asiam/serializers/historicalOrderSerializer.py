import os
from typing import List
from rest_framework import serializers
from asiam.models import Pedido,Cliente

from django.conf import settings
from django.conf.urls.static import static

class HistoricalOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pedido
        field = ('id','codi_mone','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi','codi_espe','codi_tipe','codi_user')
        exclude =['created','deleted','updated','esta_ttus']
