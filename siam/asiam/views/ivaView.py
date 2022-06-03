from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Iva
from asiam.serializers import IvaSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class IvaListView(generics.ListAPIView):
    serializer_class = IvaSerializer
    permission_classes = ()
    queryset = Iva.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class IvaCreateView(generics.CreateAPIView):
    serializer_class = IvaSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class IvaRetrieveView(generics.RetrieveAPIView):
    serializer_class = IvaSerializer
    permission_classes = ()
    queryset = Iva.get_queryset()
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

class IvaUpdateView(generics.UpdateAPIView):
    serializer_class = IvaSerializer
    permission_classes = ()
    queryset = Iva.get_queryset()
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

class IvaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = Iva.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Iva '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Iva no Registrado")

class IvaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = IvaSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Iva.get_queryset().order_by('-id')
        return queryset