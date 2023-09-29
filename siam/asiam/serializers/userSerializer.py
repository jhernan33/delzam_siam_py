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

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_superuser = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email','username','password','first_name','last_name','is_superuser','is_staff','is_active')

    def validate_password(self, value):
        return make_password(value)
    
    def validate_username(self, value):
        result_user = User.objects.all().filter(username = value)
        if result_user.count() > 0:
            raise serializers.ValidationError("Nombre de Usuario ya Registrado")
        return value
    
    def validate_email(self,value):
        result_email = User.objects.all().filter(email = value)
        if result_email.count() > 0:
            raise serializers.ValidationError("Cuenta de Correo Electronico ya Registrada")
        return value

    def create(self, validated_data):       
        user = User(username = validated_data['username'].lower(),
                    first_name = validated_data['first_name'].upper(),
                    last_name = validated_data['last_name'].upper(),
                    email = validated_data['email'].lower(),
                    password = validated_data['password'],
                    )
        user.is_superuser = False if(self.data.get('is_superuser',None) == None) else True
        user.is_staff = False if(self.data.get('is_staff',None) == None) else True
        user.is_active = False if(self.data.get('is_active',None) == None) else True
        print(user)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length= 3,max_length=150)
    password = serializers.CharField(min_length= 8,max_length=128)

    # Primero validamos los datos
    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key