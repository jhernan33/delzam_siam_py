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

from asiam.models import Ciudad, Estado
from asiam.serializers import CiudadSerializer, CiudadBasicSerializer, EstadoSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from django.http import Http404, HttpResponse


class CiudadListView(generics.ListAPIView):
    serializer_class = CiudadSerializer
    permission_classes = ()
    queryset = Ciudad.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','nomb_ciud','codi_esta__nomb_esta']
    search_fields = ['id','nomb_ciud','codi_esta__nomb_esta']
    ordering_fields = ['id','nomb_ciud','codi_esta__nomb_esta']

    def get_queryset(self):
        show = self.request.query_params.get('show',None)

        queryset = Ciudad.objects.all()
        if show =='true':
            queryset = queryset.filter(deleted__isnull=False)
        if show =='false' or show is None:
            queryset = queryset.filter(deleted__isnull=True)        

        return queryset

class CiudadCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CiudadSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            #result_city = Ciudad.get_queryset().filter(nomb_ciud = str(self.request.data.get("nomb_ciud")).strip().upper())
            #if result_city.count() == 0:
                try:
                    city = Ciudad(
                        nomb_ciud      = str(self.request.data.get("nomb_ciud")).strip().upper()
                        ,codi_esta      = Estado.get_queryset().get(id = self.request.data.get("codi_esta"))
                        ,created        = datetime.now()
                    )
                    city.save()
                    return message.SaveMessage('Registro de Ciudad guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar la Ciudad: "+str(e))
            #elif result_city.count()>0:
            #    return message.ShowMessage('Nombre de Ciudad ya Registrada')
        except Ciudad.DoesNotExist:
            return message.NotFoundMessage("Id de Ciudad no Registrado")
            

class CiudadRetrieveView(generics.RetrieveAPIView):
    permission_classes = ()
    serializer_class = CiudadSerializer
    queryset = Ciudad.get_queryset()
    lookup_field = 'id'
    
    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Ciudad.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)
        
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
            return message.NotFoundMessage("Id de Ciudad no Registrado")
        else:
            try:
                # Validate Name City
                #result_name_city = CiudadSerializer.validate_nomb_ciud(str(request.data['nomb_ciud']).upper().strip(),instance.id)
                #if result_name_city == True:
                #    return message.ShowMessage("Nombre de Ciudad ya Registrado")

                # Validate Id State
                result_state = EstadoSerializer.validate_codi_esta(request.data['codi_esta'])
                if result_state == False:
                    return message.ShowMessage("Id de Estado No Regsistrado, en la Lista de Ciudad")

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.nomb_ciud      = str('' if self.request.data.get("nomb_ciud") is None else self.request.data.get("nomb_ciud")).strip().upper()
                instance.codi_esta      = Estado.get_queryset().get(id = self.request.data.get("codi_esta"))
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                return message.UpdateMessage("Actualizado Exitosamente los Datos de la Ciudad: "+str(instance.id))
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

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
