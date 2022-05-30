from datetime import datetime
from rest_framework import serializers
from asiam.models import Familia

class FamiliaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Familia
        fields = ('id','desc_fami','abae_fami','agru_fami','created','updated','deleted')
        # read_only_fields = ('id', )

    def update(self, instance, validated_data):
        instance.updated = datetime.now()
        instance.save()
        return instance