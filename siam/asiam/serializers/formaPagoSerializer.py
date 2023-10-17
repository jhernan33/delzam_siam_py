import os
from typing import List
from rest_framework import serializers
from asiam.models import FormaPago
from django.conf import settings
from django.conf.urls.static import static

class FormaPagoSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormaPago
        field = ('id',)
        exclude =['created','updated','esta_ttus','desc_fopa','orde_fopa']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = str(instance.desc_fopa).upper()
        representation['ordering'] = instance.orde_fopa
        return representation
    
    def validate_desc_fopa(value,state, _id:None):
        if _id is not None:
            queryset = FormaPago.objects.filter(desc_fopa = str(value).lower().strip()) if state else FormaPago.get_queryset().filter(desc_fopa = str(value).lower().strip())
        else:
            queryset = FormaPago.objects.filter(desc_fopa = str(value).lower().strip()).filter(id) if state else FormaPago.get_queryset().filter(desc_fopa = str(value).lower().strip())
        
        if queryset.count() == 0:
            return False
        else:
            return True
    

class FormaPagoComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','desc_fopa','deleted','orde_fopa']

    def to_representation(self, instance):
        data = super(FormaPagoComboSerializer, self).to_representation(instance=instance)
        
        # Upper Description
        data["description"] = str(instance.desc_fopa).upper()
        return data
    
class FormaPagoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        field = ('id','desc_fopa')
        exclude = ['created','updated','esta_ttus','orde_fopa']
