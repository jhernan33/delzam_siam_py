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


from asiam.models import PedidoTipo
from asiam.serializers import PedidoTipoSerializer, PedidoTipoComboSerializer, PedidoTipoBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

from django.http.request import QueryDict


class PedidoTipoListView(generics.ListAPIView):
    serializer_class = PedidoTipoSerializer
    permission_classes = ()
    queryset = PedidoTipo.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','desc_tipe']
    ordering_fields = ['id','desc_tipe']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = PedidoTipo.objects.all()
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

class PedidoTipoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = PedidoTipoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Description
            result_description = PedidoTipoSerializer.validate_desc_tipe(request.data['description'],False)
            if result_description == False:
                try:
                    pedidoTipo = PedidoTipo(
                        desc_tipe                           = self.request.data.get("description")
                        ,orde_tipe                          = self.request.data.get("ordering")
                        ,created                            = datetime.now()
                    )
                    pedidoTipo.save()
                    return message.SaveMessage('Pedido guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar Tipo de Pedido: "+str(e))
            return message.ShowMessage("Descripcion ya Registrada")
        except PedidoTipo.DoesNotExist:
            return message.NotFoundMessage("Id de Tipo de Pedido no Registrado")
            
class PedidoTipoRetrieveView(generics.RetrieveAPIView):
    serializer_class = PedidoTipoSerializer
    permission_classes = ()
    queryset = PedidoTipo.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = PedidoTipo.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id Tipo de Pedido no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class PedidoTipoUpdateView(generics.UpdateAPIView):
    serializer_class = PedidoTipoSerializer
    permission_classes = ()
    queryset = PedidoTipo.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id Tipo de Pedido no Registrado")
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
                result_description = PedidoTipoSerializer.validate_desc_tipe(request.data['description'],state_deleted)
                if result_description == True:
                    return message.ShowMessage("Descripcion ya se encuentra Registrada")
                
                instance.desc_tipe                       = self.request.data.get("description")
                instance.orde_tipe                       = self.request.data.get("ordering")
                instance.deleted                            = isdeleted
                instance.updated                            = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"description":instance.desc_tipe,"ordering":instance.orde_tipe})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class PedidoTipoDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id' 

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                cliente = PedidoTipo.objects.get(pk=kwargs['id'])
                cliente.deleted = datetime.now()
                cliente.save()
                return message.DeleteMessage('Tipo de Pedido '+str(cliente.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id Tipo de Pedido no Registrado")
            
class PedidoTipoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = PedidoTipoComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = PedidoTipo.get_queryset().order_by('orde_tipe')
        return queryset

