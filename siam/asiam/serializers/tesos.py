from rest_framework import serializers
from asiam.models import Tesos

class TesosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tesos
        # fields = ('id','desc_tess','codi_tesc','codi_tess',)
        fields = ['codi_tess','desc_tess']
        # fields = "__all__"        
        read_only_fields = ('id', )