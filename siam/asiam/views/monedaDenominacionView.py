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


from asiam.models import Moneda, MonedaDenominacion
from asiam.serializers import MonedaDenominacionSerializer, MonedaDenominacionBasicSerializer, MonedaDenominacionComboSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from django.conf import settings
from .serviceImageView import ServiceImageView

class MonedaDenominacionListView(generics.ListAPIView):
    serializer_class = MonedaDenominacionSerializer
    permission_classes = [IsAuthenticated]
    queryset = MonedaDenominacion.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','nomb_deno','tipo_deno','valo_deno','codi_mone__desc_mone']
    ordering_fields = ['id','nomb_deno','tipo_deno','valo_deno','codi_mone__desc_mone']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = MonedaDenominacion.objects.all()
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

class MonedaDenominacionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MonedaDenominacionSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Description
            result_description = MonedaDenominacionSerializer.validate_nomb_deno(request.data['description'],False,None)
            if result_description == False:

                enviroment = os.path.realpath(settings.WEBSERVER_CURRENCY_DENOMINATION)
                ServiceImage = ServiceImageView()
                # Photo
                json_photo_currency_denomination = None
                if request.data['photo'] is not None:
                    listImagesCurrencyDenomination  = request.data['photo']
                    json_photo_currency_denomination  = ServiceImage.saveImag(listImagesCurrencyDenomination,enviroment)
                
                try:
                    currencyDenomination = MonedaDenominacion(
                        tipo_deno  = self.request.data.get("type")
                        ,nomb_deno = self.request.data.get("description")
                        ,valo_deno = self.request.data.get("currency_amount")
                        ,codi_mone = Moneda.get_queryset().get(id = self.request.data.get("currency"))
                        ,foto_deno = None if json_photo_currency_denomination is None else json_photo_currency_denomination
                        ,orde_deno = 1 if json_photo_currency_denomination is None else self.request.data.get("order")
                        ,created   = datetime.now()
                    )
                    currencyDenomination.save()
                    return message.SaveMessage('Denominación guardada Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar la Denominación: "+str(e))
            return message.ShowMessage("Nombre de la Denominación ya Registrada")
        except MonedaDenominacion.DoesNotExist:
            return message.NotFoundMessage("Id de la Denominación de Moneda no Registrado")

class MonedaDenominacionRetrieveView(generics.RetrieveAPIView):
    serializer_class = MonedaDenominacionSerializer
    permission_classes = [IsAuthenticated]
    queryset = MonedaDenominacion.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = MonedaDenominacion.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de la Denominacion de la Moneda no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class MonedaDenominacionUpdateView(generics.UpdateAPIView):
    serializer_class = MonedaDenominacionSerializer
    permission_classes = [IsAuthenticated]
    queryset = MonedaDenominacion.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de la Denominación de Moneda no Registrado")
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
                result_description = MonedaDenominacionSerializer.validate_nomb_deno(request.data['description'],state_deleted,instance.id)
                if result_description == True:
                    return message.ShowMessage("Nombre de la Denominación ya se encuentra Registrada")
            
                listImages = request.data['photo']
                enviroment = os.path.realpath(settings.WEBSERVER_CURRENCY_DENOMINATION)
                ServiceImage = ServiceImageView()
                json_photo_currency_denomination = ServiceImage.updateImage(listImages,enviroment)
                
                instance.tipo_deno = self.request.data.get("type")
                instance.nomb_deno = self.request.data.get("description")
                instance.valo_deno = self.request.data.get("currency_amount")
                instance.codi_mone = Moneda.get_queryset().get(id = self.request.data.get("currency"))
                instance.foto_deno = None if json_photo_currency_denomination is None else json_photo_currency_denomination
                instance.orde_deno = 1 if json_photo_currency_denomination is None else self.request.data.get("order")
                instance.deleted   = isdeleted
                instance.updated   = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"description":instance.nomb_deno})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class MonedaDenominacionDestroyView(generics.DestroyAPIView):
    serializer_class = MonedaDenominacionSerializer
    permission_classes = [IsAuthenticated]
    queryset = MonedaDenominacion.get_queryset()
    lookup_field = 'id'
        
    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            try:
                instance = self.get_object()
            except Exception as e:
                return message.NotFoundMessage("Id de la Denominación de Moneda no Registrado")
            else:
                with transaction.atomic():
                    currencyDenomination = MonedaDenominacion.objects.get(pk=kwargs['id'])
                    currencyDenomination.deleted = datetime.now()
                    currencyDenomination.save()
                    return message.DeleteMessage('Denominación de la Moneda '+str(currencyDenomination.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de la Denominación de Moneda no Registrada")

class MonedaDenominacionComboView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MonedaDenominacionComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = MonedaDenominacion.objects.all()
        currency = self.request.query_params.get('currency',None)
        if currency:
            return queryset.filter(codi_mone = currency)
        
        queryset = MonedaDenominacion.get_queryset().order_by('orde_deno')
        return queryset