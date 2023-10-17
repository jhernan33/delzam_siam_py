from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import Profile
from django.contrib.auth.models import User, Group, Permission, GroupManager
from asiam.serializers import UserBasicSerializer


class ProfileUserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        field = ('id','user')
        exclude = ['created','updated','esta_ttus','biography','location','birth_date','profile_picture','phone_number']

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        field = ('id','user')
        exclude =['created','updated','esta_ttus','biography','location','birth_date','profile_picture','phone_number']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = str(instance.ncta_cuen).upper()
        representation['biography'] = instance.biography
        representation['birth_date'] = instance.birth_date
        representation['profile_picture'] = instance.profile_picture
        representation['phone_number'] = instance.phone_number
        return representation
    
    """
        Validate User
    """    
    def validate_currency_date(_currency,_date,state, _id:None):
        queryset = []
        
        # Instance of currency
        _currency = Moneda.get_queryset().get(id = _currency)
        # Check Id Tasa
        if _id is not None:
            queryset = TasaCambio.objects.filter(codi_mone = _currency).filter(fech_taca = _date).exclude(id=_id) if state else TasaCambio.get_queryset().filter(codi_mone = _currency).filter(fech_taca = _date).exclude(id=_id)
        else:
            queryset = TasaCambio.objects.filter(codi_mone = _currency).filter(fech_taca = _date) if state else TasaCambio.get_queryset().filter(codi_mone = _currency).filter(fech_taca = _date)
        
        if queryset.count() == 0:
            return False
        else:
            return True
    
