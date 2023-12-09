
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import Contacto
from asiam.serializers import CategoriaContactoSerializer, ClienteSerializer, ProveedorSerializer, VendedorSerializer, NaturalSerializer, JuridicaSerializer, AccionistaSerializer

class ContactoSoloNumeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        field = ('desc_cont')
        exclude = ['id','codi_grco','codi_clie','codi_prov','codi_vend','codi_natu','codi_juri','codi_acci','deleted','created','updated','esta_ttus']

class ContactoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        field = ('id','desc_cont')
        exclude = ['codi_grco','codi_clie','codi_prov','codi_vend','codi_natu','codi_juri','codi_acci','deleted','created','updated','esta_ttus']


class ContactoSerializer(serializers.ModelSerializer):
    codi_grco = CategoriaContactoSerializer()
    codi_clie = ClienteSerializer()
    codi_prov = ProveedorSerializer()
    codi_vend = VendedorSerializer()
    codi_natu = NaturalSerializer()
    codi_juri = JuridicaSerializer()
    codi_acci = AccionistaSerializer()
    
    class Meta:
        model = Contacto
        field = ('id','desc_cont','codi_grco','codi_clie','codi_prov','codi_vend','codi_natu','codi_juri','codi_acci','deleted')
        exclude =['created','updated','esta_ttus']
    
    
