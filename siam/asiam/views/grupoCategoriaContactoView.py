from datetime import datetime
import re
from unittest import result
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from asiam.models import GrupoCategoriaContacto, CategoriaContacto
from asiam.serializers import GrupoCategoriaContactoSerializer, GrupoCategoriaContactoBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage

class GrupoCategoriaContactoListView(generics.ListAPIView):
    serializer_class = GrupoCategoriaContactoSerializer
    permission_classes = ()
    queryset = GrupoCategoriaContacto.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ('id','desc_grup')
    ordering_fields = ('id', 'desc_grup')
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = GrupoCategoriaContacto.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)

class GrupoCategoriaContactoCreateView(generics.CreateAPIView):
    serializer_class = GrupoCategoriaContactoSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            name_ctco = self.request.data.get("desc_grup").upper().strip()
            codi_ctco = CategoriaContacto.get_queryset().get(id=self.request.data.get("codi_ctco")) 
            result_Grupo = GrupoCategoriaContacto.objects.filter(desc_grup = name_ctco)
            
            if result_Grupo.count() <= 0:
                try:
                    GrupoCategoriaContacto = GrupoCategoriaContacto(
                        desc_grup = name_ctco,
                        codi_ctco = codi_ctco,
                        created  = datetime.now()
                    )
                    GrupoCategoriaContacto.save()
                    return message.SaveMessage({"id":GrupoCategoriaContacto.id,"desc_grup":GrupoCategoriaContacto.desc_grup})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar el Grupo de Categoria de Contacto: "+str(e))
            elif result_Grupo.count()>0:
                return message.ShowMessage({'information':name_ctco,'message':"Ya Registrada"})
        except GrupoCategoriaContacto.DoesNotExist:
            return message.NotFoundMessage("Id de Grupo de Categoria de Contacto no Registrado")
         
class GrupoCategoriaContactoRetrieveView(generics.RetrieveAPIView):
    serializer_class = GrupoCategoriaContactoSerializer
    permission_classes = ()
    queryset = GrupoCategoriaContacto.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = GrupoCategoriaContacto.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Grupo de Categoria de Contacto no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class GrupoCategoriaContactoUpdateView(generics.UpdateAPIView):
    serializer_class = GrupoCategoriaContactoSerializer
    permission_classes = ()
    queryset = GrupoCategoriaContacto.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Grupo de Categoria de Contacto no Registrada")
        else:
            try:
                # Validate Description GrupoCategoriaContacto
                result_Grupo = GrupoCategoriaContacto.objects.filter(desc_grup = self.request.data.get("desc_grup").upper().strip())
                if result_Grupo.count() > 0:
                    if result_Grupo[0].id != instance.id:
                        return message.ShowMessage("Descripcion de Grupo de Categoria de Contacto ya Registrada con el ID:"+str(result_Grupo[0].id))

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.desc_grup = request.data['desc_grup'].upper().strip()
                instance.codi_ctco = CategoriaContacto.get_queryset().get(id=self.request.data.get("codi_ctco")) 
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"desc_grup":instance.desc_grup})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class GrupoCategoriaContactoDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = GrupoCategoriaContacto.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_grupo = GrupoCategoriaContacto.get_queryset().get(id=kwargs['id'])
            result_grupo.deleted = datetime.now()
            result_grupo.save()
            return message.DeleteMessage('Grupo de Categoria de Contacto '+str(result_grupo.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Grupo de Categoria de Contacto no Registrada")

# Drop Down
class GrupoCategoriaContactoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = GrupoCategoriaContactoBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = GrupoCategoriaContacto.objects.all().order_by('id')
        show = self.request.query_params.get('show',None)
        category = self.request.query_params.get('category',None)
        
        # Parameter Category Contact
        if category:
            return queryset.filter(codi_ctco = category).filter(deleted__isnull=True)
            
        if show =='true':
            return queryset.all()
        if show =='false' or show is None:
            return queryset.filter(deleted__isnull=True)
        