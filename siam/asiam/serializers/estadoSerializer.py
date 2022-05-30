from datetime import datetime
from rest_framework import serializers
from asiam.models import Estado

class EstadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estado
        field = ('id','codi_pais')
        exclude =['created','updated','deleted','esta_ttus']

    def update(self, instance, validated_data):
        instance.updated = datetime.now()
        instance.save()
        return instance