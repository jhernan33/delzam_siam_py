from datetime import datetime
from email import message
import json
from django.shortcuts import render
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from yaml import serialize

from asiam.models import Ciudad
from asiam.serializers import CiudadSerializer, CiudadBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from django.http import Http404, HttpResponse


class CiudadListView(generics.ListAPIView):
    serializer_class = CiudadSerializer
    permission_classes = ()
    queryset = Ciudad.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class CiudadCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CiudadSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)
            

class CiudadRetrieveView(generics.RetrieveAPIView):
    permission_classes = ()
    serializer_class = CiudadSerializer
    queryset = Ciudad.get_queryset()
    lookup_field = 'id'
      
    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ciudad no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)
    
class CiudadUpdateView(generics.UpdateAPIView):
    serializer_class = CiudadSerializer
    permission_classes = ()
    queryset = Ciudad.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ciudad no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Ciudad")

class CiudadDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id'  

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = Ciudad.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Ciudad '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Ciudad no Registrada")


class CiudadComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CiudadBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.query_params.get('codi_esta') == None:
            queryset = Ciudad.get_queryset().all()
        else:
            queryset = Ciudad.get_queryset().filter(codi_esta = self.request.query_params.get('codi_esta')).order_by('nomb_ciud')
        return queryset
