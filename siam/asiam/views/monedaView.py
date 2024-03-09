import os
from datetime import datetime
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist


from asiam.models import Moneda, Pais
from asiam.serializers import MonedaSerializer, MonedaBasicSerializer, MonedaComboSerializer, MonedaTasaSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from django.conf import settings
from .serviceImageView import ServiceImageView

class MonedaListView(generics.ListAPIView):
    serializer_class = MonedaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Moneda.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','desc_mone','simb_mone','codi_mone','codi_pais__nomb_pais']
    ordering_fields = ['id','desc_mone','simb_mone','codi_mone','codi_pais__nomb_pais']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Moneda.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        field = self.request.query_params.get('field',None)
        value = self.request.query_params.get('value',None)
        if field is not None and value is not None:
            if field=='codi_natu':
                queryset = queryset.filter(codi_natu=value)

        return queryset.filter(deleted__isnull=True)

class MonedaCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MonedaSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Description
            result_description = MonedaSerializer.validate_desc_mone(request.data['description'],False,None)
            if result_description == False:

                enviroment = os.path.realpath(settings.WEBSERVER_CURRENCY)
                ServiceImage = ServiceImageView()
                # Logo
                json_photo_currency = None
                if request.data['logo'] is not None:
                    listImagesCurrency  = request.data['logo']
                    json_photo_currency  = ServiceImage.saveImag(listImagesCurrency,enviroment)
                try:
                    moneda = Moneda(
                        desc_mone   = self.request.data.get("description")
                        ,codi_pais  = Pais.get_queryset().get(id = self.request.data.get("country"))
                        ,simb_mone  = self.request.data.get("symbol")
                        ,codi_mone  = self.request.data.get("code")
                        ,logo_mone  = None if json_photo_currency is None else json_photo_currency
                        ,created    = datetime.now()
                    )
                    moneda.save()
                    return message.SaveMessage('Moneda guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar Moneda: "+str(e))
            return message.ShowMessage("Descripcion ya Registrada")
        except Moneda.DoesNotExist:
            return message.NotFoundMessage("Id de Moneda no Registrado")

class MonedaRetrieveView(generics.RetrieveAPIView):
    serializer_class = MonedaTasaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Moneda.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Moneda.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Moneda no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class MonedaUpdateView(generics.UpdateAPIView):
    serializer_class = MonedaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Moneda.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Moneda no Registrado")
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
                result_description = MonedaSerializer.validate_desc_mone(request.data['description'],state_deleted,instance.id)
                if result_description == True:
                    return message.ShowMessage("Descripcion ya se encuentra Registrada")
            
                listImages = request.data['logo']
                enviroment = os.path.realpath(settings.WEBSERVER_CURRENCY)
                ServiceImage = ServiceImageView()
                json_photo_currency = ServiceImage.updateImage(listImages,enviroment)
                
                instance.desc_mone = self.request.data.get("description")
                instance.codi_pais = Pais.get_queryset().get(id = self.request.data.get("country"))
                instance.simb_mone = self.request.data.get("symbol")
                instance.codi_mone = self.request.data.get("code")
                instance.logo_mone = json_photo_currency
                instance.deleted   = isdeleted
                instance.updated   = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"description":instance.desc_mone})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class MonedaDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                moneda = Moneda.objects.get(pk=kwargs['id'])
                moneda.deleted = datetime.now()
                moneda.save()
                return message.DeleteMessage('Moneda '+str(moneda.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Moneda no Registrado")

class MonedaComboView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MonedaComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Moneda.get_queryset().order_by('orde_mone')
        return queryset