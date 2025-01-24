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


from asiam.models import PedidoEstatus
from asiam.serializers import PedidoEstatusSerializer, PedidoEstatusComboSerializer, PedidoEstatusBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

from django.http.request import QueryDict


class PedidoEstatusListView(generics.ListAPIView):
    serializer_class = PedidoEstatusSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoEstatus.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','desc_esta']
    ordering_fields = ['id','desc_esta']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = PedidoEstatus.objects.all()
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

class PedidoEstatusCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoEstatusSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Description
            result_description = PedidoEstatusSerializer.validate_desc_esta(request.data['description'],False,None)
            if result_description == False:
                try:
                    pedidoEstatus = PedidoEstatus(
                        desc_esta                           = self.request.data.get("description")
                        ,orde_esta                          = self.request.data.get("ordering")
                        ,created                            = datetime.now()
                    )
                    pedidoEstatus.save()
                    return message.SaveMessage('Estatus de Pedido guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar Estatus de Pedido: "+str(e))
            return message.ShowMessage("Descripcion ya Registrada")
        except PedidoEstatus.DoesNotExist:
            return message.NotFoundMessage("Id de Estatus de Pedido no Registrado")
            
class PedidoEstatusRetrieveView(generics.RetrieveAPIView):
    serializer_class = PedidoEstatusSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoEstatus.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = PedidoEstatus.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id Estatus de Pedido no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class PedidoEstatusUpdateView(generics.UpdateAPIView):
    serializer_class = PedidoEstatusSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoEstatus.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id Estatus de Pedido no Registrado")
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
                result_description = PedidoEstatusSerializer.validate_desc_esta(request.data['description'],state_deleted,instance.id)
                if result_description == True:
                    return message.ShowMessage("Descripcion ya se encuentra Registrada")
                
                instance.desc_esta                       = self.request.data.get("description")
                instance.orde_esta                       = self.request.data.get("ordering")
                instance.deleted                            = isdeleted
                instance.updated                            = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"description":instance.desc_esta,"ordering":instance.orde_esta})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class PedidoEstatusDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' 

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                cliente = PedidoEstatus.objects.get(pk=kwargs['id'])
                cliente.deleted = datetime.now()
                cliente.save()
                return message.DeleteMessage('Estatus de Pedido '+str(cliente.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id Estatus de Pedido no Registrado")
            
class PedidoEstatusComboView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoEstatusComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        history = self.request.query_params.get('history')
        if history =='true':
            _orderStatus = (7,8)
            # Convert Str to Tuple
            _result = tuple(map(int, _orderStatus.split(',')))
            return queryset.filter(deleted__isnull=False).filter(in__in = _result)
        queryset = PedidoEstatus.get_queryset().order_by('orde_esta')
        return queryset

