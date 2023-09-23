from datetime import datetime
from os import environ
import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http.response import JsonResponse
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser 
from rest_framework import status


from asiam.models import FormaPago
from asiam.serializers import FormaPagoSerializer, FormaPagoComboSerializer, FormaPagoBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

from django.http.request import QueryDict


class FormaPagoListView(generics.ListAPIView):
    serializer_class = FormaPagoSerializer
    permission_classes = ()
    queryset = FormaPago.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','desc_fopa']
    ordering_fields = ['id','desc_fopa']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = FormaPago.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        field = self.request.query_params.get('field',None)
        value = self.request.query_params.get('value',None)
        if field is not None and value is not None:
            if field=='codi_natu':
                queryset = queryset.filter(codi_natu=value)

        return queryset.filter(deleted__isnull=True)

class FormaPagoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = FormaPagoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Description
            result_description = FormaPagoSerializer.validate_desc_fopa(request.data['description'],False,None)
            if result_description == False:
                try:
                    formaPago = FormaPago(
                        desc_fopa                           = self.request.data.get("description")
                        ,created                            = datetime.now()
                    )
                    formaPago.save()
                    return message.SaveMessage('Forma de Pago guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar Forma de Pago: "+str(e))
            return message.ShowMessage("Descripcion Forma de Pago ya Registrada")
        except FormaPago.DoesNotExist:
            return message.NotFoundMessage("Id de Forma de Pago no Registrado")
            
class FormaPagoRetrieveView(generics.RetrieveAPIView):
    serializer_class = FormaPagoSerializer
    permission_classes = ()
    queryset = FormaPago.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = FormaPago.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Forma de Pago no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class FormaPagoUpdateView(generics.UpdateAPIView):
    serializer_class = FormaPagoSerializer
    permission_classes = ()
    queryset = FormaPago.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Forma de Pago no Registrado")
        else:
            try:
                # State Deleted
                state_deleted = None
                if instance.deleted:
                    state_deleted = True
                
                Deleted = request.data['erased']
                if Deleted:                    
                    isdeleted = datetime.now()
                else:    
                    isdeleted = None
                
                # Validate Description
                result_description = FormaPagoSerializer.validate_desc_fopa(request.data['description'],state_deleted,instance.id)
                if result_description == True:
                    return message.ShowMessage("Descripcion de Forma de Pago ya se encuentra Registrada")
                
                instance.desc_fopa                       = self.request.data.get("description")
                instance.deleted                            = isdeleted
                instance.updated                            = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"description":instance.desc_fopa})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class FormaPagoDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id' 

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                formaPago = FormaPago.objects.get(pk=kwargs['id'])
                formaPago.deleted = datetime.now()
                formaPago.save()
                return message.DeleteMessage('Forma de Pago '+str(formaPago.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Forma de Pago no Registrado")
            
class FormaPagoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = FormaPagoComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = FormaPago.get_queryset().order_by('orde_esta')
        return queryset

