from os import environ
import os
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist


from asiam.models import Banco, Cuenta
from asiam.serializers import BancoSerializer, BancoComboSerializer, BancoBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

class BancoListView(generics.ListAPIView):
    serializer_class = BancoSerializer
    permission_classes = ()
    queryset = Banco.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','desc_banc']
    ordering_fields = ['id','desc_banc']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Banco.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

class BancoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = BancoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Description
            result_description = BancoSerializer.validate_desc_banc(request.data['description'],False,None)
            if result_description == False:
                
                enviroment = os.path.realpath(settings.WEBSERVER_BANK)
                ServiceImage = ServiceImageView()
                json_logo_banc = None
                if request.data['logo'] is not None:
                    listImagesbank  = request.data['logo']
                    json_logo_banc  = ServiceImage.saveImag(listImagesbank,enviroment)
                try:
                    banco = Banco(
                        desc_banc                           = self.request.data.get("description"),
                        logo_banc                           = json_logo_banc,
                        created                            = datetime.now()
                    )
                    banco.save()
                    return message.SaveMessage('Banco guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar Banco: "+str(e))
            return message.ShowMessage("Descripcion ya Registrada")
        except Banco.DoesNotExist:
            return message.NotFoundMessage("Id de Banco no Registrado")

class BancoRetrieveView(generics.RetrieveAPIView):
    serializer_class = BancoSerializer
    permission_classes = ()
    queryset = Banco.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Banco.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Banco no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class BancoUpdateView(generics.UpdateAPIView):
    serializer_class = BancoSerializer
    permission_classes = ()
    queryset = Banco.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Banco no Registrado")
        else:
            try:
                json_logo_banc = None
                if request.data['logo'] is not None:
                    enviroment = os.path.realpath(settings.WEBSERVER_BANK)
                    ServiceImage = ServiceImageView()
                    listImagesbank  = request.data['logo']
                    json_logo_banc  = ServiceImage.updateImage(listImagesbank,enviroment)

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
                result_description = BancoSerializer.validate_desc_banc(request.data['description'],state_deleted,instance.id)
                if result_description == True:
                    return message.ShowMessage("Descripcion ya se encuentra Registrada")
                instance.desc_banc = self.request.data.get("description")
                instance.deleted   = isdeleted
                instance.logo_banc = json_logo_banc
                instance.updated   = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"description":instance.desc_banc})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class BancoDestroyView(generics.DestroyAPIView):
    serializer_class = BancoSerializer
    permission_classes = ()
    queryset = Banco.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Delete Bank Account
                cuenta = Cuenta.get_queryset().filter(codi_banc = kwargs['id'])
                if cuenta.count()<=0:
                    # Delete Bank
                    banco = Banco.get_queryset().get(id=kwargs['id'])
                    banco.deleted = datetime.now()
                    banco.save()
                    return message.DeleteMessage('Banco '+str(banco.id))
                else:
                    return message.ShowMessage('Banco no se Puede Eliminar, porque tiene cuentas activas')
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Banco no Registrado")

class BancoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = BancoComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Banco.get_queryset().order_by('desc_banc')
        return queryset