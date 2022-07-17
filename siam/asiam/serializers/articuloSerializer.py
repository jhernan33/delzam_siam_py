import os
from typing import List
from rest_framework import serializers
from asiam.models import Articulo
from asiam.serializers import SubFamiliaSerializer
from django.conf import settings
from django.conf.urls.static import static

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentArticle = os.path.realpath(settings.WEBSERVER_ARTICLE)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentArticle+obj['image'];
            return value

    def to_internal_value(self, data):
        return data

class ArticuloSerializer(serializers.ModelSerializer):
    family = serializers.ReadOnlyField(source='codi_sufa.codi_fami.id')
    subfamilia = serializers.ReadOnlyField(source='codi_sufa.desc_sufa')
    compraPresentacion = serializers.ReadOnlyField(source='codc_pres.desc_pres')
    ventaPresentacion = serializers.ReadOnlyField(source='codv_pres.desc_pres')
    ivaValor = serializers.ReadOnlyField(source='codi_ivti.desc_ivag')
    foto_arti = JSONSerializerField()
    # total_images = serializers.IntegerField(source='id__count')

    class Meta:
        model = Articulo
        field = ('id','codi_arti','idae_arti','desc_arti','coba_arti','cmin_arti','cmax_arti'
        ,'por1_arti','por2_arti','por3_arti','ppre_arti','codi_sufa','foto_arti','exgr_arti'
        ,'codc_pres','codv_pres','capc_arti','capv_arti','proc_arti','codi_ivti','familia','subfamilia','compraPresentacion','ventaPresentacion','ivaValor')
        exclude =['created','updated','deleted','esta_ttus']
    
        desc_arti = serializers.CharField(trim_whitespace=False)
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # totals_images = serializers.SerializerMethodField
    #     print(instance)
    #     # representation['countImages'] = instance.foto_arti__count
    #     return representation

    # def get_totals_images(self,obj):
    #     # return serializers.IntegerField(source='foto_arti.count',read_only=True)
    #     print(obj.foto_arti.count())
    #     return obj.foto_arti.count()