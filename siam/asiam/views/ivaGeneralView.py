from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from asiam.models import Iva,IvaGeneral
from asiam.serializers import IvaGeneralSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class IvaGeneralListView(generics.ListAPIView):
    serializer_class = IvaGeneralSerializer
    permission_classes = ()
    queryset = IvaGeneral.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','desc_ivag']
    search_fields = ['id','desc_ivag']
    ordering_fields = ['desc_ivag']
    ordering = ['desc_ivag']


class IvaGeneralCreateView(generics.CreateAPIView):
    serializer_class = IvaGeneralSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class IvaGeneralRetrieveView(generics.RetrieveAPIView):
    serializer_class = IvaGeneralSerializer
    permission_classes = ()
    queryset = IvaGeneral.get_queryset()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de IVA no Registrado")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class IvaGeneralUpdateView(generics.UpdateAPIView):
    serializer_class = IvaGeneralSerializer
    permission_classes = ()
    queryset = IvaGeneral.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de IVA no Registrado")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar IVA")   

class IvaGeneralDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = IvaGeneral.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Iva '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Iva no Registrado")

class IvaGeneralComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = IvaGeneralSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = IvaGeneral.get_queryset().order_by('-id')
        return queryset