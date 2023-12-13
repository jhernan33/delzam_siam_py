from os import environ
import os
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist


from asiam.models import PedidoMensaje, PedidoTipo
from asiam.serializers import PedidoMensajeSerializer, PedidoMensajeComboSerializer, PedidoMensajeBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class PedidoMensajeListView(generics.ListAPIView):
    serializer_class = PedidoMensajeSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoMensaje.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','desc_mens']
    ordering_fields = ['id','desc_mens']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = PedidoMensaje.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

class PedidoMensajeCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoMensajeSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Description
            if request.data['description'] is None:
                return message.RequiredMessage("Descripción")
            
            result_description = PedidoMensajeSerializer.validate_desc_mens(request.data['description'],False,None)
            if result_description == False:
                
                orderType_id = None
                # Validate Id Order Message
                if 'orderType' in request.data:
                    orderType_id = request.data['orderType']
                    result_orderType = PedidoMensajeSerializer.validate_OrderType(orderType_id)
                    if result_orderType == False:
                        return message.NotFoundMessage("Codigo de Tipo Pedido no Registrado")
                
                try:
                    pedidomensaje = PedidoMensaje(
                        desc_mens = self.request.data.get("description"),
                        codi_tipe = PedidoTipo.getInstanceOrderType(orderType_id),
                        pred_mens = False if self.request.data.get("predetermined") is None else True,
                        created   = datetime.now()
                    )
                    pedidomensaje.save()
                    # Check Menssage Predetermined
                    if eval(str(self.request.data.get("predetermined"))) is True:
                        PedidoMensaje.get_queryset().exclude(id = pedidomensaje.id).update(pred_mens = False)
                    return message.SaveMessage('Mensaje guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar Mensaje: "+str(e))
            return message.ShowMessage("Descripcion ya Registrada")
        except PedidoMensaje.DoesNotExist:
            return message.NotFoundMessage("Id de Mensaje no Registrado")

class PedidoMensajeRetrieveView(generics.RetrieveAPIView):
    serializer_class = PedidoMensajeSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoMensaje.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = PedidoMensaje.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Mensaje no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class PedidoMensajeUpdateView(generics.UpdateAPIView):
    serializer_class = PedidoMensajeSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoMensaje.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Mensaje no Registrado")
        else:
            try:
                orderType_id = None
                # Validate Id Order Message
                if 'orderType' in request.data:
                    orderType_id = request.data['orderType']
                    result_orderType = PedidoMensajeSerializer.validate_OrderType(orderType_id)
                    if result_orderType == False:
                        return message.NotFoundMessage("Codigo de Tipo Pedido no Registrado")

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
                result_description = PedidoMensajeSerializer.validate_desc_mens(request.data['description'],state_deleted,instance.id)
                if result_description == True:
                    return message.ShowMessage("Descripcion ya se encuentra Registrada")
                instance.desc_mens = self.request.data.get("description")
                instance.codi_tipe = orderType_id
                instance.pred_mens = False if self.request.data.get("predetermined") is None else True,
                instance.deleted   = isdeleted
                instance.updated   = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"description":instance.desc_mens})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class PedidoMensajeDestroyView(generics.DestroyAPIView):
    serializer_class = PedidoMensajeSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoMensaje.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Delete Order Message
                orderMessage = PedidoMensaje.get_queryset().get(id=kwargs['id'])
                orderMessage.deleted = datetime.now()
                orderMessage.save()
                return message.DeleteMessage('Mensaje '+str(PedidoMensaje.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Mensaje no Registrado")

class PedidoMensajeComboView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoMensajeComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = PedidoMensaje.get_queryset().order_by('id')
        return queryset