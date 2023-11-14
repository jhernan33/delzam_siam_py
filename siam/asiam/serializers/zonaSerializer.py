from rest_framework import serializers
from asiam.models import Zona, Ruta

class ZonaBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        field = ('id','orde_zona','desc_zona','deleted')
        exclude = ['created','updated','esta_ttus']

    def to_representation(self, instance):
        from asiam.serializers import RutaBasicSerializer

        representation = super().to_representation(instance)
        zone = Zona.get_queryset().filter(id=instance.id).values('desc_zona')
        
        # Routes
        queryset = Ruta.get_queryset().filter(codi_zona__in = str(instance.id)).order_by('posi_ruta')
        result_routes = RutaBasicSerializer(queryset, many=True).data
        representation['routes'] = result_routes
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
        data['route_count'] = Ruta.get_queryset().filter(codi_zona__in = str(instance.id)).count()
        return data

class ZonaComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        field = ['id','description']
        exclude = exclude = ['created','updated','deleted','esta_ttus','desc_zona']

    def to_representation(self, instance):
        data = super(ZonaComboSerializer, self).to_representation(instance=instance)
        data["description"] = instance.desc_zona.upper().strip()
        return data