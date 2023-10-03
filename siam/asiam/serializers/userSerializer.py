from dataclasses import fields
import email
from unittest.util import _MAX_LENGTH
from wsgiref import validate
from defer import return_value
from httplib2 import Response
from pkg_resources import require
from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from yaml import serialize

class SignupSerializer(serializers.ModelSerializer):
    """override create method to change the password into hash."""
    def create(self, validated_data):
            validated_data["password"] = make_password(validated_data.get("password"))
            return super(SignupSerializer, self).create(validated_data)
    class Meta:
            model = User
            fields = ['username','password','is_superuser','first_name','last_name','email']

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username','password']