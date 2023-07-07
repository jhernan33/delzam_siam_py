from dataclasses import fields
from datetime import datetime
from warnings import filters
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from psycopg2 import Timestamp
from pytz import timezone

from rest_framework import status
from rest_framework import filters as df
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from asiam.models import Familia
from asiam.serializers import FamiliaSerializer, FamiliaComboSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage


class FamiliaListView(generics.ListAPIView):
    serializer_class = FamiliaSerializer
    permission_classes = []
    queryset = Familia.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','desc_fami','abae_fami','agru_fami']
    search_fields = ['id','desc_fami','abae_fami','agru_fami']
    ordering_fields = ['desc_fami','abae_fami']
    ordering = ['desc_fami']

class FamiliaCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = FamiliaSerializer    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)


class FamiliaRetrieveView(generics.RetrieveAPIView):
    serializer_class = FamiliaSerializer
    permission_classes = []
    queryset = Familia.get_queryset()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Familia no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class FamiliaUpdateView(generics.UpdateAPIView):
    serializer_class = FamiliaSerializer
    permission_classes = ()
    queryset = Familia.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Familia no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Familia")

class FamiliaDestroyView(generics.DestroyAPIView):
    permission_classes = []
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_familia = Familia.get_queryset().get(id=kwargs['id'])
            result_familia.deleted = datetime.now()
            result_familia.save()
            return message.DeleteMessage('Familia '+str(result_familia.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Familia no Registrada")

class FamiliaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = FamiliaComboSerializer
    # lookup_field = 'id'

    def get_queryset(self):
        queryset = Familia.get_queryset().order_by('desc_fami')
        return queryset

class FamiliaRestore(generics.UpdateAPIView):
    serializer_class = FamiliaSerializer
    permission_classes = ()
    queryset = Familia.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Familia no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(deleted = None)
                return message.RestoreMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Restaurar Familia")