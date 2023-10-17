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
        representation['user'] = instance.user.id
        representation['biography'] = instance.biography
        representation['birth_date'] = instance.birth_date
        representation['profile_picture'] = instance.profile_picture
        representation['phone_number'] = instance.phone_number
        return representation
    
    """
        Validate Profile
    """    
    def validate_profile(state, _id:None):
        queryset = []
        
        # Check id
        if _id is not None:
            queryset = Profile.objects.filter(id = _id) if state else Profile.objects.filter(id = _id)
        if queryset.count() == 0:
            return False
        else:
            return True
    
