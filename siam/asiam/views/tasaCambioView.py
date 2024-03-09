from os import environ
import os
from django.conf import settings
from datetime import datetime, date
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist


from asiam.models import Banco, Cuenta, TasaCambio, Moneda
from asiam.serializers import TasaCambioBasicSerializer, TasaCambioComboSerializer, TasaCambioSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

from datetime import datetime

class TasaCambioListView(generics.ListAPIView):
    serializer_class = TasaCambioSerializer
    permission_classes = [IsAuthenticated]
    queryset = TasaCambio.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','valo_taca','fech_taca']
    ordering_fields = ['id','valo_taca','fech_taca']
    ordering = ['-fech_taca']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = TasaCambio.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

class TasaCambioCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TasaCambioSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage

        serializer = self.serializer_class.validateData(data=request.data)
        if serializer:
            try:
                date_format = '%Y-%m-%d %H:%M'
                tasa = TasaCambio(
                    codi_mone   = Moneda.getInstanceCurrency(self.request.data.get("currency")),
                    fech_taca   = datetime.strptime( self.request.data.get("date"),date_format),
                    valo_taca   = self.request.data.get("value"),
                    obse_taca   = self.request.data.get("observations"),
                    tipo_taca   = self.request.data.get("type"),
                    codi_mone_to = Moneda.getInstanceCurrency(self.request.data.get("currencyTo")),
                    created = datetime.now()
                )
                tasa.save()
                return message.SaveMessage('Tasa de Cambio guardada Exitosamente')
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Guardar la Tasa de Cambio: "+str(e))
        

class TasaCambioRetrieveView(generics.RetrieveAPIView):
    serializer_class = TasaCambioSerializer
    permission_classes = [IsAuthenticated]
    queryset = TasaCambio.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = TasaCambio.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Tasa de Cambio no Registrada")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class TasaCambioUpdateView(generics.UpdateAPIView):
    serializer_class = TasaCambioSerializer
    permission_classes = [IsAuthenticated]
    queryset = TasaCambio.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        serializer = self.serializer_class.validateData(data=request.data)
        if serializer:
            try:
                instance = self.get_object()
            except Exception as e:
                return message.NotFoundMessage("Id de Tasa de Cambio no Registrada")
            else:
                try:
                    date_format = '%Y-%m-%d %H:%M:%S'
                    # State Deleted
                    state_deleted = None
                    if instance.deleted:
                        state_deleted = True
                    
                    Deleted = request.data['erased']
                    if Deleted:                    
                        isdeleted = datetime.now()
                    else:    
                        isdeleted = None
                    
                    _currency = Moneda.getInstanceCurrency(self.request.data.get("currency"))
                    _currencyTo = Moneda.getInstanceCurrency(self.request.data.get("currencyTo"))
                    
                    instance.fech_taca = datetime.strptime( self.request.data.get("date"),date_format)
                    instance.valo_taca = self.request.data.get("value")
                    instance.codi_mone = _currency
                    instance.obse_taca = self.request.data.get("observations")
                    instance.codi_mone_to = _currencyTo
                    instance.deleted = isdeleted
                    instance.updated = datetime.now()
                    instance.save()
                    
                    return message.UpdateMessage({"id":instance.id,"Exchange Rate":instance.valo_taca})
                    
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class TasaCambioDestroyView(generics.DestroyAPIView):
    serializer_class = TasaCambioSerializer
    permission_classes = [IsAuthenticated]
    queryset = TasaCambio.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Delete Exchange Rate
                tasa = TasaCambio.get_queryset().get(id = kwargs['id'])
                if tasa:
                    tasa.deleted = datetime.now()
                    tasa.save()
                    return message.DeleteMessage('Tasa de Cambio: '+str(tasa.id))
                else:
                    return message.ShowMessage('Tasa de Cambio no Registrada')
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Tasa de Cambio no Registrado")

class TasaCambioComboView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TasaCambioComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = TasaCambio.get_queryset().order_by('valo_taca')
        return queryset