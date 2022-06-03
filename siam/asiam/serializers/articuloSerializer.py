from rest_framework import serializers
from asiam.models import Articulo

class ArticuloSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articulo
        field = ('id','codi_arti','idae_arti','desc_arti','coba_arti','cmin_arti','cmax_arti'
        ,'por1_arti','por2_arti','por3_arti','ppre_arti','codi_sufa','foto_arti','exgr_arti'
        ,'codc_pres','codv_pres','capc_arti','capv_arti','proc_arti','codi_ivti')
        exclude =['created','updated','deleted','esta_ttus']
        