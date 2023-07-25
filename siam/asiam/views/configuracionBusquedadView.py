from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import ConfiguracionBusquedad
from asiam.serializers import ConfiguracionBusquedadSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ConfiguracionBusquedadListView(generics.ListAPIView):
    serializer_class = ConfiguracionBusquedadSerializer
    permission_classes = ()
    queryset = ConfiguracionBusquedad.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id',]
    search_fields = ['id',]
    ordering_fields = ['id',]

    def get_queryset(self):
        show = self.request.query_params.get('show',None)

        queryset = ConfiguracionBusquedad.objects.all()
        
        if show =='true':
            queryset = queryset.filter(deleted__isnull=False)
        if show =='false' or show is None:
            queryset = queryset.filter(deleted__isnull=True)        

        field = self.request.query_params.get('field',None)
        value = self.request.query_params.get('value',None)
        if field is not None and value is not None:
            queryset = queryset.filter(field=value)
        
        return queryset



class ConfiguracionBusquedadCreateView(generics.CreateAPIView):
    serializer_class = ConfiguracionBusquedadSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class ConfiguracionBusquedadRetrieveView(generics.RetrieveAPIView):
    serializer_class = ConfiguracionBusquedadSerializer
    permission_classes = ()
    queryset = ConfiguracionBusquedad.get_queryset()
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

class ConfiguracionBusquedadUpdateView(generics.UpdateAPIView):
    serializer_class = ConfiguracionBusquedadSerializer
    permission_classes = ()
    queryset = ConfiguracionBusquedad.get_queryset()
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

class ConfiguracionBusquedadDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = ConfiguracionBusquedad.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Iva '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Iva no Registrado")

class ConfiguracionBusquedadComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ConfiguracionBusquedadSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = ConfiguracionBusquedad.get_queryset().order_by('-id')
        return queryset