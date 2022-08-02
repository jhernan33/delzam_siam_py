import os
from typing import List
from rest_framework import serializers
from asiam.models import ArticuloProveedor, Articulo, Proveedor
from asiam.serializers import ArticuloSerializer, ProveedorSerializer
from django.conf import settings
from django.conf.urls.static import static

class ArticuloProveedorSerializer(serializers.ModelSerializer):
    codi_arti = ArticuloSerializer()
    codi_prov = ProveedorSerializer()

    class Meta:
        model = ArticuloProveedor
        field = ('id','codi_arti','codi_prov','codi_arti_prov','obse_arti_prov','deleted')
        exclude =['created','updated','esta_ttus']
    
    def validate_codi_arti(value):
        queryset = Articulo.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True
    
    def validate_codi_prov(value):
        queryset = Proveedor.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True