from datetime import datetime
from rest_framework import serializers
from asiam.models import TipoEmpresa

class TipoEmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoEmpresa
        fields = ['id','desc_tiem']

    def update(self, instance, validated_data):
        instance.updated = datetime.now()
        instance.save()
        return instance
