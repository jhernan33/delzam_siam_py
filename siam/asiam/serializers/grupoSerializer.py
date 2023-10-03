from rest_framework import serializers
from django.contrib.auth.models import User, Group

class GrupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id','name')
        read_only_fields = ('id',)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = str(instance.name).upper()
        return representation