from rest_framework import serializersfrom asiam.models import Monedasclass MonedasSerializer(serializers.ModelSerializer):    class Meta:        model = Monedas        fields = ('id','desc_mone',)        read_only_fields = ('id', )