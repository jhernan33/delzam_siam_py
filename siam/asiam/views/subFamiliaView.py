from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import filters as df
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import SubFamilia
from asiam.serializers import SubFamiliaSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage

class SubFamiliaListView(generics.ListAPIView):
    serializer_class = SubFamiliaSerializer
    permission_classes = []
    queryset = SubFamilia.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','desc_sufa','abae_sufa','agru_sufa']
    search_fields = ['id','desc_sufa','abae_sufa','agru_sufa']
    ordering_fields = ['desc_sufa','abae_sufa']
    ordering = ['desc_sufa']

class SubFamiliaCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = SubFamiliaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class SubFamiliaRetrieveView(generics.RetrieveAPIView):
    serializer_class = SubFamiliaSerializer
    permission_classes = []
    queryset = SubFamilia.get_queryset()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de SubFamilia no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class SubFamiliaUpdateView(generics.UpdateAPIView):
    serializer_class = SubFamiliaSerializer
    permission_classes = []
    queryset = SubFamilia.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de SubFamilia no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar SubFamilia")

class SubFamiliaDestroyView(generics.DestroyAPIView):
    permission_classes = []
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_subFamilia = SubFamilia.get_queryset().get(id=kwargs['id'])
            result_subFamilia.deleted = datetime.now()
            result_subFamilia.save()
            return message.DeleteMessage('SubFamilia '+str(result_subFamilia.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de SubFamilia no Registrada")

class SubFamiliaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = SubFamiliaSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = SubFamilia.get_queryset().order_by('-id')
        return queryset
