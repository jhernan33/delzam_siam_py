from os import environ
import os
from django.conf import settings
from datetime import datetime, date
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Natural, Cobrador
from asiam.serializers import CobradorBasicSerializer, CobradorComboSerializer, CobradorSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

from datetime import datetime


class CobradorListView(generics.ListAPIView):
    serializer_class = CobradorSerializer
    permission_classes = ()
    queryset = Cobrador.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','fein_cobr','tili_cobr','fvli_cobr','feli_cobr','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena']
    ordering_fields = ['id','fein_cobr','tili_cobr','fvli_cobr','feli_cobr','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Cobrador.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

class CobradorCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CobradorSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            enviroment = os.path.realpath(settings.WEBSERVER_COLLECTOR)
            ServiceImage = ServiceImageView()
            date_format = '%Y-%m-%d'
            
            # Photo
            json_photo_collector = None
            if request.data['photo'] is not None:
                listImagesCollector  = request.data['photo']
                json_photo_collector  = ServiceImage.saveImag(listImagesCollector,enviroment)

            collector = Cobrador(
                codi_natu = Natural.getInstanceNatural(self.request.data.get("natural")),
                fein_cobr = datetime.strptime( self.request.data.get("dateOfEntry"),date_format),
                foto_cobr = None if json_photo_collector is None else json_photo_collector,
                lice_cobr = self.request.data.get("licence"),
                feli_cobr = datetime.strptime(self.request.data.get("expeditionDate",date_format)),
                fvli_cobr = datetime.strptime(self.request.data.get("dueDate"),date_format),
                tili_cobr = self.request.data.get("typeLicence"),
                created = datetime.now()
            )
            collector.save()
            return message.SaveMessage('Cobrador guardado Exitosamente')
        except Exception as e:
            return message.ErrorMessage("Error al Intentar Guardar la Cobrador: "+str(e))

class CobradorRetrieveView(generics.RetrieveAPIView):
    serializer_class = CobradorSerializer
    permission_classes = ()
    queryset = Cobrador.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Cobrador.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Cobrador no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class CobradorUpdateView(generics.UpdateAPIView):
    serializer_class = CobradorSerializer
    permission_classes = ()
    queryset = Cobrador.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Cobrador no Registrado")
        else:
            try:
                enviroment = os.path.realpath(settings.WEBSERVER_SELLER)
                ServiceImage = ServiceImageView()

                date_format = '%Y-%m-%d'
                # State Deleted
                state_deleted = None
                if instance.deleted:
                    state_deleted = True
                
                Deleted = request.data['erased']
                if Deleted:                    
                    isdeleted = datetime.now()
                else:    
                    isdeleted = None
                
                _natural = Natural.getInstanceNatural(self.request.data.get("natural"))
                # Photo
                json_photo_collector = None
                if request.data['photo'] is not None:
                    listImagesCollector  = request.data['photo']
                    json_photo_collector  = ServiceImage.saveImag(listImagesCollector,enviroment)
                
                instance.codi_natu = _natural
                instance.fein_cobr = datetime.strptime( self.request.data.get("dateOfEntry"),date_format)
                instance.foto_cobr = json_photo_collector
                instance.lice_cobr = self.request.data.get("licence")
                instance.feli_cobr = datetime.strptime(self.request.data.get("expeditionDate",date_format))
                instance.fvli_cobr = datetime.strptime(self.request.data.get("dueDate"),date_format)
                instance.tili_cobr = self.request.data.get("typeLicence")
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class CobradorDestroyView(generics.DestroyAPIView):
    serializer_class = CobradorSerializer
    permission_classes = ()
    queryset = Cobrador.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Delete Exchange Rate
                collector = Cobrador.get_queryset().get(id = kwargs['id'])
                if collector:
                    collector.deleted = datetime.now()
                    collector.save()
                    return message.DeleteMessage('Cobrador: '+str(collector.id))
                else:
                    return message.ShowMessage('Cobrador no Registrado')
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Cobrador no Registrado")

class CobradorComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CobradorComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Cobrador.get_queryset().order_by('valo_taca')
        return queryset