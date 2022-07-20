from datetime import datetime
from os import environ
import os
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Proveedor
from asiam.serializers import ProveedorSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView
from django.conf import settings
from django.conf.urls.static import static


class ProveedorListView(generics.ListAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    queryset = Proveedor.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','codi_natu','codi_juri','codi_repr']
    search_fields = ['id','codi_natu','codi_juri','codi_repr']
    ordering_fields = ['id','codi_natu','codi_juri','codi_repr']
    ordering = ['codi_natu']


class ProveedorCreateView(generics.CreateAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        listImages = request.data['foto_prov']
        enviroment = os.path.realpath(settings.WEBSERVER_ARTICLE)
        ServiceImage = ServiceImageView()
        json_images = ServiceImage.saveImag(listImages,enviroment)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if json_images is None:
            serializer.validated_data['foto_prov'] = json_images
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class ProveedorRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    queryset = Proveedor.get_queryset()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Proveedor no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)


class ProveedorUpdateView(generics.UpdateAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    queryset = Proveedor.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Proveedor no Registrado")
        else:
            listImages = request.data['foto_prov']
            enviroment = os.path.realpath(settings.WEBSERVER_ARTICLE)
            ServiceImage = ServiceImageView()
            json_images = ServiceImage.updateImage(listImages,enviroment)

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now(), foto_prov = json_images)
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Proveedor")

class ProveedorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Proveedor.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = Proveedor.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Proveedor '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Proveedor no Registrado")

class ProveedorComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ProveedorSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Proveedor.get_queryset().order_by('-id')
        return queryset

class ProveedorRestore(generics.UpdateAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    queryset = Proveedor.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Presentacion no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(deleted = None)
                return message.RestoreMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Restaurar Presentacion")