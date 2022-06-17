from rest_framework import serializers
from asiam.models import Articulo

class ArticuloSerializer(serializers.ModelSerializer):
    subfamilia = serializers.ReadOnlyField(source='codi_sufa.desc_sufa')
    compraPresentacion = serializers.ReadOnlyField(source='codc_pres.desc_pres')
    ventaPresentacion = serializers.ReadOnlyField(source='codv_pres.desc_pres')
    ivaValor = serializers.ReadOnlyField(source='codi_ivti.desc_ivag')

    class Meta:
        model = Articulo
        field = ('id','codi_arti','idae_arti','desc_arti','coba_arti','cmin_arti','cmax_arti'
        ,'por1_arti','por2_arti','por3_arti','ppre_arti','codi_sufa','foto_arti','exgr_arti'
        ,'codc_pres','codv_pres','capc_arti','capv_arti','proc_arti','codi_ivti','subfamilia','compraPresentacion','ventaPresentacion','ivaValor')
        exclude =['created','updated','deleted','esta_ttus']
    
        desc_arti = serializers.CharField(trim_whitespace=False)