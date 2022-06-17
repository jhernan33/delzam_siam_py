from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Articulo
from asiam.serializers import ArticuloSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage

class ArticuloListView(generics.ListAPIView):
    serializer_class = ArticuloSerializer
    permission_classes = ()
    queryset = Articulo.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','desc_arti','idae_arti']
    search_fields = ['id','desc_arti','idae_arti']
    ordering_fields = ['desc_arti','idae_arti']
    ordering = ['desc_arti']


class ArticuloCreateView(generics.CreateAPIView):
    serializer_class = ArticuloSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class ArticuloRetrieveView(generics.RetrieveAPIView):
    serializer_class = ArticuloSerializer
    permission_classes = ()
    queryset = Articulo.get_queryset()
    lookup_field = 'id'

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
    permission_classes = ()
    queryset = Articulo.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Articulo no Registrado")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Articulo")

class ArticuloDestroyView(generics.DestroyAPIView):
    permission_classes = ()
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
    permission_classes = []
    serializer_class = ArticuloSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Articulo.get_queryset().order_by('-id')
        return queryset