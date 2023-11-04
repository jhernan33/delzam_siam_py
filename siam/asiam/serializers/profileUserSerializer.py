import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework import serializers

from asiam.models import Profile
from django.contrib.auth.models import User, Group, Permission, GroupManager
from asiam.serializers import UserBasicSerializer

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentArticle = os.path.realpath(settings.WEBSERVER_USER)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentArticle+obj['image']
            return value

    def to_internal_value(self, data):
        return data
    
class ProfileUserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        field = ('id','user')
        exclude = ['created','updated','esta_ttus','biography','location','birth_date','profile_picture','phone_number']

class ProfileUserSerializer(serializers.ModelSerializer):
    profile_picture = JSONSerializerField()
    class Meta:
        model = Profile
        field = ('id','user','profile_picture')
        exclude =['created','updated','esta_ttus','biography','location','birth_date','phone_number']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.id
        representation['biography'] = instance.biography
        representation['birth_date'] = instance.birth_date
        representation['phone_number'] = instance.phone_number
        if instance.profile_picture is None:
            place = settings.WEBSERVER_IMAGES
            enviromentArticle = os.path.realpath(settings.WEBSERVER_USER)[1:]+'/'
            representation['profile_picture'] = place+enviromentArticle+'base.jpeg'
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
    
