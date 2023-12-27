import os
from typing import List
from rest_framework import serializers
from asiam.models import Articulo, ArticuloProveedor
from asiam.serializers.articuloProveedorSerializer import ArticuloProveedorSerializerBasics
from django.conf import settings
from django.conf.urls.static import static

class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentArticle = os.path.realpath(settings.WEBSERVER_ARTICLE)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentArticle+obj['image']
            return value

    def to_internal_value(self, data):
        return data

class ArticuloComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ('id','desc_arti','codi_sufa')


class ArticuloSerializer(serializers.ModelSerializer):
    family = serializers.ReadOnlyField(source='codi_sufa.codi_fami.id')
    familyDescription = serializers.ReadOnlyField(source='codi_sufa.codi_fami.desc_fami')
    subfamilia = serializers.ReadOnlyField(source='codi_sufa.desc_sufa')
    compraPresentacion = serializers.ReadOnlyField(source='codc_pres.desc_pres')
    ventaPresentacion = serializers.ReadOnlyField(source='codv_pres.desc_pres')
    ivaValor = serializers.ReadOnlyField(source='codi_ivti.desc_ivag')
    foto_arti = JSONSerializerField()
    # total_images = serializers.IntegerField(source='id__count')

    class Meta:
        model = Articulo
        field = ('id','codi_arti','idae_arti','desc_arti','coba_arti','cmin_arti','cmax_arti'
        ,'por1_arti','por2_arti','por3_arti','por4_arti','ppre_arti','codi_sufa','foto_arti','exgr_arti'
        ,'codc_pres','codv_pres','capc_arti','capv_arti','proc_arti','codi_ivti','familia','subfamilia','compraPresentacion','ventaPresentacion','ivaValor','cos1_arti','deleted')
        exclude =['created','updated','esta_ttus']
    
        desc_arti = serializers.CharField(trim_whitespace=False)
    
    def to_representation(self, instance):
        route = None
        representation = super().to_representation(instance)
        representation['cos1_arti'] = 0 if instance.por1_arti is None  else (instance.ppre_arti*(instance.por1_arti/100))+instance.ppre_arti
        representation['cos2_arti'] = 0 if instance.por2_arti is None  else instance.ppre_arti*(instance.por2_arti/100)+instance.ppre_arti
        representation['cos3_arti'] = 0 if instance.por3_arti is None  else instance.ppre_arti*(instance.por3_arti/100)+instance.ppre_arti
        representation['cos4_arti'] = 0 if instance.por4_arti is None  else instance.ppre_arti*(instance.por4_arti/100)+instance.ppre_arti
        representation['price'] = Articulo.toPriceTheProduct(instance.id, None)
        representation['quantity_on_hand'] = 0 if instance.exis_arti is None else instance.exis_arti
        # Price
        if self.context.get('request') is not None:
            route = self.context['request'].GET.get('route')
        
        representation['price'] = Articulo.toPriceTheProduct(instance.id,route)
        # Supplier
        queryset = ArticuloProveedor.objects.filter(codi_arti=instance.id)
        result = ArticuloProveedorSerializerBasics(queryset, many=True).data
        representation['supplier'] = {"data":result}
        return representation