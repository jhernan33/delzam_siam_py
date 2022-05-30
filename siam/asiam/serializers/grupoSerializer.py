from rest_framework import serializers
from django.contrib.auth.models import User, Group

class GrupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id','name')
        read_only_fields = ('id', )