import django_filters
from asiam.models import Pedido, Cliente

class PedidoFilter(django_filters.FilterSet):
    # codi_clie = django_filters.CharFilter(method='filter_custom')

    class Meta:
        model = Pedido
        fields = ('codi_clie__codi_natu__prno_pena'
                ,'codi_clie__codi_natu__seno_pena'
                ,'codi_clie__codi_natu__prap_pena'
                ,'codi_clie__codi_natu__seap_pena'
                ,'fech_pedi','codi_espe','codi_tipe','codi_mone')
    
    # def filter_custom(self, queryset, name, value):
    #     print("Data=====>",queryset,name,value)
    #     return queryset.filter(codi_clie__codi_natu__prno_pena__contains=value)