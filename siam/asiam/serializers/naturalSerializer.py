from rest_framework import serializers
from asiam.serializers import CiudadSerializer, SectorSerializer
from asiam.models import Natural

class NaturalSerializer(serializers.ModelSerializer):
    codi_ciud = CiudadSerializer()
    codi_sect = SectorSerializer()

    class Meta:
        model = Natural
        field = ['id','naci_pena','cedu_pena','prno_pena','seno_pena','prap_pena','seap_pena','sexo_pena','fena_pena','dire_pena','riff_pena','nomb_apel','nombre_completo','apellido_completo','riff_pena','codi_ciud']
        exclude =['created','updated','deleted','esta_ttus']