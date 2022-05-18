from rest_framework import serializers
from asiam.models import Cliente

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = ('id','fein_clie','codi_ante','cred_clie','plzr_clie','prde_clie','prau_clie','codi_vend','codi_natu','codi_juri','foto_clie')
        # fields = ['id','desc_fami','agru_fami']
        # fields = "__all__"        
        read_only_fields = ('id', )