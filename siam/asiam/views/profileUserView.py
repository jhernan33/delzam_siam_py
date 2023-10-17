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


from asiam.models import Profile
from django.contrib.auth.models import User, Group, Permission, GroupManager
from asiam.serializers import ProfileUserSerializer, ProfileUserBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class ProfileUserListView(generics.ListAPIView):
    serializer_class = ProfileUserSerializer
    permission_classes = ()
    queryset = Profile.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','user','biography','location','birth_date','phone_number']
    ordering_fields = ['id','user','biography','location','birth_date','phone_number']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Profile.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

class ProfileUserCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = ProfileUserSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Profile
            result_user_profile = ProfileUserSerializer.validate_currency_date(request.data['currency'],self.request.data.get("date"),False,None)
            if result_user_profile == False:
                try:
                    tasa = Profile(
                        fech_taca   = self.request.data.get("date"),
                        valo_taca   = self.request.data.get("value"),
                        codi_mone   = Moneda.getInstanceCurrency(self.request.data.get("currency")),
                        obse_taca   = self.request.data.get("observations"),
                        created = datetime.now()
                    )
                    tasa.save()
                    return message.SaveMessage('Tasa de Cambio guardada Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar la Tasa de Cambio: "+str(e))
            return message.ShowMessage("Tasa de Cambio para la Moneda ya Registrada")
        except Profile.DoesNotExist:
            return message.NotFoundMessage("Id de Tasa de Cambio no Registrado")

class ProfileUserRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProfileUserSerializer
    permission_classes = ()
    queryset = Profile.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Profile.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Perfil no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class ProfileUserpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUserSerializer
    permission_classes = ()
    queryset = Profile.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Tasa de Cambio no Registrada")
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
                result_exchage_rate = ProfileUserSerializer.validate_currency_date(request.data['currency'],self.request.data.get("date"),state_deleted,instance.id)
                if result_exchage_rate == True:
                    return message.ShowMessage("Tasa de Cambio ya Registrada para una Moneda")
                
                _currency = Moneda.getInstanceCurrency(self.request.data.get("currency"))
                
                instance.fech_taca = self.request.data.get("date")
                instance.valo_taca = self.request.data.get("value")
                instance.codi_mone = _currency
                instance.obse_taca = self.request.data.get("observations")
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"Exchange Rate":instance.valo_taca})
                
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class ProfileUserDestroyView(generics.DestroyAPIView):
    serializer_class = ProfileUserSerializer
    permission_classes = ()
    queryset = Profile.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Delete Profile
                profile = Profile.get_queryset().get(id = kwargs['id'])
                if profile:
                    profile.deleted = datetime.now()
                    profile.save()
                # Delete User
                    return message.DeleteMessage('Perfil: '+str(profile.id))
                else:
                    return message.ShowMessage('Perfil no Registrado')
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Perfil no Registrado")
