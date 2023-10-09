from datetime import datetime
from unittest import result

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import filters as df

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate,login,logout

from asiam.serializers import GrupoSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage


class GrupoListView(generics.ListAPIView):
    serializer_class = GrupoSerializer
    permission_classes = []
    queryset = Group.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class GrupoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = GrupoSerializer    

    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            name_group = str(self.request.data.get("name")).lower().strip()
            result_group = Group.objects.filter(name = name_group)
            if result_group.count() <= 0:
                try:
                    group = Group(
                        name = name_group,
                    )
                    group.save()
                    return message.SaveMessage({"id":group.id,"name":str(group.name).upper()})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar el Grupo: "+str(e))
            elif result_group.count()>0:
                return message.ShowMessage({'information':name_group,'message':"Ya Registrada"})
        except Group.DoesNotExist:
            return message.NotFoundMessage("Id de Grupo no Registrado")

class GrupoRetrieveView(generics.RetrieveAPIView):
    serializer_class = GrupoSerializer
    permission_classes = ()
    queryset = Group.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Group.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Grupo no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class GrupoUpdateView(generics.UpdateAPIView):
    serializer_class = GrupoSerializer
    permission_classes = ()
    queryset = Group.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Grupo no Registrado")
        else:
            try:
                instance.name = str(request.data['name']).lower().strip()
                instance.save()

                return message.UpdateMessage({"id":instance.id,"name":str(instance.name).upper()})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class GrupoDestroyView(generics.DestroyAPIView):
    permission_classes =  []
    # queryset = Group.objects
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_group = Group.objects.filter(id=kwargs['id'])
            # result_group = {group.name: group.user_set.values_list('id', flat=True) for group in Group.objects.all()}
            
            if result_group.count()<= 0:
                return message.NotFoundMessage("Id de Grupo no Registrado")

            # Search User Groups and Group Permissions
            # print(result_group)
            # result_user = request.user.groups.filter(name__in = [result_group])
            # result_user = request.user.groups.values_list('name', flat=True).first()
            # result_user = request.user.groups.values_list('name', flat=True).first()
            # result_user = request.user.groups.through.objects.get(id=1)
            Group.user_set.through.objects.get(id=kwargs['id'])
            return message.ShowMessage("No se Puede Eliminar porque esta siendo utilizado el Grupo")
        except ObjectDoesNotExist:
            Group.objects.filter(id=kwargs['id']).delete()
            return message.DeleteMessage('Grupo '+str(kwargs['id']))

class GrupoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = GrupoSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Group.objects.all()
        return queryset