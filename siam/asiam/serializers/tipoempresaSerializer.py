from datetime import datetime
from rest_framework import serializers
from asiam.models import TipoEmpresa

class TipoEmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoEmpresa
        field = ['id','desc_tiem']
        exclude =['created','updated','deleted','esta_ttus']
