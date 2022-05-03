from rest_framework import serializers
from asiam.models import Tesol, Tesos
from asiam.serializers.tesos import (
    TesosSerializer
)

class TesolSerializer(serializers.ModelSerializer):
    codi_tess = TesosSerializer()
    # queryset = Tesos.objects.all()
    # codi_tess = serializers.SerializerMethodField()

    def get_codi_tess(self, project):
        return TesosSerializer(project.codi_tess()).data

    class Meta:
        model = Tesol
        # fields = ('id','fech_tesl','mont_tesl','codi_tess')h
        fields = "__all__"

    # def to_representation(self,instance):
    #     return{
    #         'id': instance.id,
    #         'fecha': instance.fech_tesl,
    #         'monto': instance.mont_tesl,
    #         # 'item': instance.codi_tess,
    #         # 'codi_tess': instance.Tesos.codi_tess if instance.Tesos is not None else '',
    #     }
