from os import environ
import base64
import os
from django.core.files import File 
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
from .serviceImageView import ServiceImageView

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
            result_user_profile = ProfileUserSerializer.validate_profile(False,self.request.data.get("user"))
            if result_user_profile == True:
                try:
                    profile = Profile(
                        User    = User.objects.get(id = self.request.data.get("user")),
                        biography   = self.request.data.get("biography"),
                        location    = self.request.data.get("location"),
                        birth_date  = self.request.data.get("birth_date"),
                        profile_picture  = self.request.data.get("profile_picture"),
                        phone_number = self.request.data.get("phone_number"),
                        created = datetime.now()
                    )
                    profile.save()
                    return message.SaveMessage('Perfil guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar el Perfil: "+str(e))
            return message.ShowMessage("Perfil ya Registrada para el Usuario")
        except Profile.DoesNotExist:
            return message.NotFoundMessage("Id de Perfil no Registrado")

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

class ProfileUserUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUserSerializer
    permission_classes = ()
    queryset = Profile.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Perfil no Registrado")
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
                
                # Validate Profile
                result_profile = ProfileUserSerializer.validate_profile(state_deleted,instance.id)
                if result_profile == False:
                    return message.NotFoundMessage("Id de Perfil no Registrado")
                
                # Save Profile Picture
                enviroment = os.path.realpath(settings.WEBSERVER_USER)
                ServiceImage = ServiceImageView()
                json_profile_picture = None
                if request.data['picture'] is not None:
                    list_profile_picture  = request.data['picture']
                    json_profile_picture  = ServiceImage.updateImage(list_profile_picture,enviroment)
                    print("Perfillllllllllllll===>",json_profile_picture)

                # Instance User
                _user = User.objects.get(id = self.request.data.get("user"))
                
                instance.user = _user
                instance.biography = self.request.data.get("biography")
                instance.location = self.request.data.get("location")
                instance.birth_date = self.request.data.get("birth_date")
                instance.profile_picture = json_profile_picture
                instance.phone_number = self.request.data.get("phone_number")
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id})
                
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
