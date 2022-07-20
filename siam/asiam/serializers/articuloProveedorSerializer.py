import os
from typing import List
from rest_framework import serializers
from asiam.models import Articulo
from asiam.serializers import SubFamiliaSerializer
from django.conf import settings
from django.conf.urls.static import static

class ArticuloProveedorSerializer(serializers.ModelSerializer):
    articulo = serializers.ReadOnlyField(source='codi_arti.desc_arti')
    proveedor = serializers.ReadOnlyField(source='codi.desc_pres')

    class Meta:
        model = Articulo
        field = ('id','codi_arti','codi_prov','codi_arti_prov','obse_arti_prov','articulo','proveedor')
        exclude =['created','updated','deleted','esta_ttus']