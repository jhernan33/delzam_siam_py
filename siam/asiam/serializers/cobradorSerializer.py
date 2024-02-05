from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import Natural, Cobrador
from asiam.serializers.naturalSerializer import NaturalSerializer

class CobradorBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobrador
        field = ('id','codi_natu')
        exclude = ['created','updated','esta_ttus','fein_cobr','foto_cobr','lice_cobr','feli_cobr','fvli_cobr','tili_cobr']

class CobradorSerializer(serializers.ModelSerializer):
    codi_natu = NaturalSerializer()

    class Meta:
        model = Cobrador
        field = ('id','codi_natu')
        exclude = ['created','updated','esta_ttus','fein_cobr','foto_cobr','lice_cobr','feli_cobr','fvli_cobr','tili_cobr']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['dateOfEntry'] = instance.fein_cobr
        representation['photo'] = instance.foto_cobr
        representation['licence'] = instance.lice_cobr
        representation['expeditionDate'] = instance.feli_cobr
        representation['dueDate'] = instance.fvli_cobr
        representation['typeLicence'] = instance.tili_cobr
        return representation
    
class CobradorComboSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cobrador
        field = ['id','description']
        exclude = ['created','updated','deleted','esta_ttus','codi_natu','fein_cobr','foto_cobr','lice_cobr','feli_cobr','fvli_cobr','tili_cobr']

    def to_representation(self, instance):
        data = super(CobradorComboSerializer, self).to_representation(instance=instance)
        description = None

        natural =  Natural.get_queryset().filter(id =instance.codi_natu.id)
        if natural.count()>0:
            description = str(natural[0].prno_pena+' '+natural[0].seno_pena +' '+natural[0].prap_pena+' '+natural[0].seap_pena).upper()
        # Description
        data["description"] = description
        return data
    