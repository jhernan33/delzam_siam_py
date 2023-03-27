from rest_framework import serializers
from asiam.models import Zona

class ZonaBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        field = ('id')
        exclude = ['created','updated','deleted','esta_ttus','desc_zona','orde_zona']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        zone = Zona.get_queryset().filter(id=instance.id).values('desc_zona')
        
        representation['description'] = zone[0]['desc_zona'].strip().upper()
        return representation


class ZonaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zona
        field = ('id','desc_zona','deleted')
        exclude =['created','updated','esta_ttus']
    
    def to_representation(self, instance):
        data = super(ZonaSerializer, self).to_representation(instance=instance)
        data['desc_zona'] = data['desc_zona'].upper().strip() if data['desc_zona'] else data['desc_zona']
        return data