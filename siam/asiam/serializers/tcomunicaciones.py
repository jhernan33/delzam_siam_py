from rest_framework import serializersfrom asiam.models import Tcomunicacionesclass TcomunicacionesSerializer(serializers.ModelSerializer):    class Meta:        model = Tcomunicaciones        fields = ('id','desc_tico',)        read_only_fields = ('id', )