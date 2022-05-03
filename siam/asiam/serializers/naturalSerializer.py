from rest_framework import serializers
from asiam.models import Natural

class NaturalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Natural
        fields = ('id','naci_pena','cedu_pena','prno_pena','seno_pena','prap_pena','seap_pena','sexo_pena','fena_pena','dire_pena','riff_pena','nomb_apel','nombre_completo','apellido_completo','riff_pena',)
        read_only_fields = ('id','codi_ciud_id','codi_sect_id')