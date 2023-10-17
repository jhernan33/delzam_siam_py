from datetime import datetime
from os import environ
import os
from django.http import JsonResponse
from django.shortcuts import render
from requests import delete
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Articulo
from asiam.serializers import ArticuloSerializer, ArticuloComboSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView
from django.conf import settings
from django.conf.urls.static import static


class ArticuloListView(generics.ListAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    queryset = Articulo.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','desc_arti','idae_arti','codi_arti','codi_sufa__desc_sufa','codi_sufa__abae_sufa','codi_sufa__codi_fami__desc_fami','codi_sufa__codi_fami__abae_fami']
    search_fields = ['id','desc_arti','idae_arti','codi_arti','codi_sufa__desc_sufa','codi_sufa__abae_sufa','codi_sufa__codi_fami__desc_fami','codi_sufa__codi_fami__abae_fami']
    ordering_fields = ['id','desc_arti','idae_arti','codi_arti','codi_sufa__desc_sufa','codi_sufa__abae_sufa','codi_sufa__codi_fami__desc_fami','codi_sufa__codi_fami__abae_fami']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Articulo.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)

class ArticuloCreateView(generics.CreateAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    
    def create(self, request, *args, **kwargs):
        listImages = request.data['foto_arti']
        enviroment = os.path.realpath(settings.WEBSERVER_ARTICLE)
        ServiceImage = ServiceImageView()
        json_images = ServiceImage.saveImag(listImages,enviroment)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['foto_arti'] = json_images
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class ArticuloRetrieveView(generics.RetrieveAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    queryset = Articulo.get_queryset()
    lookup_field = 'id'
    
    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Articulo.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Articulo no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)


class ArticuloUpdateView(generics.UpdateAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    queryset = Articulo.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Articulo no Registrado")
        else:
            listImages = request.data['foto_arti']
            enviroment = os.path.realpath(settings.WEBSERVER_ARTICLE)
            ServiceImage = ServiceImageView()
            json_images = ServiceImage.updateImage(listImages,enviroment)
            Deleted = request.data['erased']
            if Deleted:
                isdeleted = datetime.now()
            else:
                isdeleted = None
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now(), foto_arti = json_images, deleted = isdeleted)
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Articulo")

class ArticuloDestroyView(generics.DestroyAPIView):
    permission_classes =  []
    queryset = Articulo.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = Articulo.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Articulo '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Articulo no Registrado")

class ArticuloComboView(generics.ListAPIView):
    permission_classes =  []
    serializer_class = ArticuloComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Articulo.get_queryset().order_by('desc_arti')
        return queryset
    
    def get_queryset(self):
        if self.request.query_params.get('subfamily') == None:
            queryset = Articulo.get_queryset().order_by('desc_arti')
        else:
            queryset = Articulo.get_queryset().filter(codi_sufa=self.request.query_params.get('subfamily')).order_by('desc_arti')
        return queryset