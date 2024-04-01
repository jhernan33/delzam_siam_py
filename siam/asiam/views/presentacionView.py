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

from asiam.models import Presentacion
from asiam.serializers import PresentacionSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage


class PresentacionListView(generics.ListAPIView):
    serializer_class = PresentacionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Presentacion.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','desc_pres','tipo_pres','abre_pres']
    search_fields = ['id','desc_pres','tipo_pres','abre_pres']
    ordering_fields = ['desc_pres','tipo_pres','id']
    ordering = ['desc_pres']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Presentacion.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

class PresentacionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PresentacionSerializer    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)


class PresentacionRetrieveView(generics.RetrieveAPIView):
    serializer_class = PresentacionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Presentacion.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Presentacion.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)
    
    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Presentacion no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class PresentacionUpdateView(generics.UpdateAPIView):
    serializer_class = PresentacionSerializer
    permission_classes = ()
    queryset = Presentacion.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Presentacion no Registrada")
        else:
            try:
                # State Deleted
                state_deleted = None
                if instance.deleted:
                    state_deleted = True
                
                Deleted = request.data['erased']
                if Deleted:                    
                    isdeleted = datetime.now()
                else:    
                    isdeleted = None

                # Validate Description
                result_description = PresentacionSerializer.validate_desc_pres(request.data['desc_pres'],state_deleted,instance.id)
                if result_description == True:
                    return message.ShowMessage("Descripcion ya se encuentra Registrada")
                instance.desc_pres = self.request.data.get("desc_pres")
                instance.abre_pres = self.request.data.get("abre_pres")
                instance.tipo_pres = self.request.data.get("tipo_pres")
                instance.deleted   = isdeleted
                instance.updated   = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"desc_pres":instance.desc_pres})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

            # serializer = self.get_serializer(instance, data=request.data, partial=True)
            # if serializer.is_valid():
            #     serializer.save(updated = datetime.now())
            #     return message.UpdateMessage(serializer.data)
            # else:
            #     return message.ErrorMessage("Error al Intentar Actualizar Presentacion")

class PresentacionDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_Presentacion = Presentacion.get_queryset().get(id=kwargs['id'])
            result_Presentacion.deleted = datetime.now()
            result_Presentacion.save()
            return message.DeleteMessage('Presentacion '+str(result_Presentacion.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Presentacion no Registrada")

class PresentacionComboView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PresentacionSerializer
    # lookup_field = 'id'
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    ordering_fields = ['desc_pres','tipo_pres','abre_pres','id']

    def get_queryset(self):
        queryset = Presentacion.get_queryset()
        return queryset

class PresentacionRestore(generics.UpdateAPIView):
    serializer_class = PresentacionSerializer
    permission_classes = ()
    queryset = Presentacion.objects.all()
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