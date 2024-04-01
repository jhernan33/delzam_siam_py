from datetime import datetime
from rest_framework import serializers
from asiam.models import Presentacion

class PresentacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentacion
        field = ('id','desc_pres','tipo_pres','abre_pres','deleted')
        exclude =['created','updated','esta_ttus']

    """
        Validate Description Presentation
    """    
    def validate_desc_pres(value,state, _id:None):
        if _id is not None:
            queryset = Presentacion.objects.filter(desc_pres = str(value).lower().strip()).exclude(id=_id) if state else Presentacion.get_queryset().filter(desc_pres = str(value).lower().strip()).exclude(id=_id)
        else:
            queryset = Presentacion.objects.filter(desc_pres = str(value).lower().strip()) if state else Presentacion.get_queryset().filter(desc_pres = str(value).lower().strip())
        
        if queryset.count() == 0:
            return False
        else:
            return True
    