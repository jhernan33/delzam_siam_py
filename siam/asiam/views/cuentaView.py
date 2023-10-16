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
from asiam.serializers import CuentaBasicSerializer, CuentaSerializer, CuentaComboSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class CuentaListView(generics.ListAPIView):
    serializer_class = CuentaSerializer
    permission_classes = ()
    queryset = Cuenta.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','ncta_cuen']
    ordering_fields = ['id','ncta_cuen']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Cuenta.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

class CuentaCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CuentaSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Account Number
            result_account_number = CuentaSerializer.validate_ncta_cuen(request.data['account_number'],self.request.data.get("bank"),False,None)
            
            if result_account_number == False:
                try:
                    cuenta = Cuenta(
                        ncta_cuen   = self.request.data.get("account_number"),
                        fape_cuen   = self.request.data.get("opening_date"),
                        tipo_cuen   = self.request.data.get("type"),
                        codi_banc   = Banco.get_queryset().get(id = self.request.data.get("bank")),
                        created = datetime.now()
                    )
                    cuenta.save()
                    return message.SaveMessage('Cuenta guardada Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar la Cuenta: "+str(e))
            return message.ShowMessage("Numero de Cuenta ya Registrada en el Banco")
        except Cuenta.DoesNotExist:
            return message.NotFoundMessage("Id de Cuenta no Registrado")

class CuentaRetrieveView(generics.RetrieveAPIView):
    serializer_class = CuentaSerializer
    permission_classes = ()
    queryset = Cuenta.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Cuenta.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Cuenta no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class CuentaUpdateView(generics.UpdateAPIView):
    serializer_class = CuentaSerializer
    permission_classes = ()
    queryset = Cuenta.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Cuenta no Registrado")
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
                result_account_number = CuentaSerializer.validate_ncta_cuen(request.data['account_number'],self.request.data.get("bank"),state_deleted,instance.id)
                if result_account_number == True:
                    return message.ShowMessage("Numero de Cuenta ya Registrada en el Banco")
                
                instance.ncta_cuen = self.request.data.get("account_number")
                instance.fape_cuen = self.request.data.get("date_create"),
                instance.tipo_cuen = self.request.data.get("type"),
                instance.codi_banc = Banco.objects.get(id=self.request.data.get("bank")),
                instance.deleted   = isdeleted
                instance.updated   = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"Account Number":instance.ncta_cuen})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class CuentaDestroyView(generics.DestroyAPIView):
    serializer_class = CuentaSerializer
    permission_classes = ()
    queryset = Cuenta.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Delete Bank Account
                cuenta = Cuenta.get_queryset().filter(codi_banc = kwargs['id'])
                if cuenta.count()<=0:
                    # Delete Bank
                    cuenta = Cuenta.get_queryset().get(id=kwargs['id'])
                    cuenta.deleted = datetime.now()
                    cuenta.save()
                    return message.DeleteMessage('Cuenta '+str(cuenta.id))
                else:
                    return message.ShowMessage('Cuenta no se Puede Eliminar, porque tiene cuentas activas')
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Cuenta no Registrado")

class CuentaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CuentaComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Cuenta.get_queryset().order_by('ncta_cuen')
        return queryset