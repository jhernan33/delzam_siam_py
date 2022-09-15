from datetime import datetime
import re
from unittest import result
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from asiam.models import CategoriaContacto
from asiam.serializers import CategoriaContactoSerializer, CategoriaContactoBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage

class CategoriaContactoListView(generics.ListAPIView):
    serializer_class = CategoriaContactoSerializer
    permission_classes = ()
    queryset = CategoriaContacto.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ('id','desc_ctco')
    ordering_fields = ('id', 'desc_ctco')
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = CategoriaContacto.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)

class CategoriaContactoCreateView(generics.CreateAPIView):
    serializer_class = CategoriaContactoSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            name_ctco = self.request.data.get("desc_ctco").upper().strip()
            result_categoria_Contacto = CategoriaContacto.objects.filter(desc_ctco = name_ctco)
            
            if result_categoria_Contacto.count() <= 0:
                try:
                    categoriaContacto = CategoriaContacto(
                        desc_ctco = name_ctco,
                        created  = datetime.now()
                    )
                    categoriaContacto.save()
                    return message.SaveMessage({"id":categoriaContacto.id,"desc_ctco":categoriaContacto.desc_ctco})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar La Categoria de Contacto: "+str(e))
            elif result_categoria_Contacto.count()>0:
                return message.ShowMessage({'information':name_ctco,'message':"Ya Registrada"})
        except Zona.DoesNotExist:
            return message.NotFoundMessage("Id de Categoria de Contacto no Registrado")
         
class CategoriaContactoRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategoriaContactoSerializer
    permission_classes = ()
    queryset = CategoriaContacto.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = CategoriaContacto.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Categoria de Contacto no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class CategoriaContactoUpdateView(generics.UpdateAPIView):
    serializer_class = CategoriaContactoSerializer
    permission_classes = ()
    queryset = CategoriaContacto.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Categoria de Contacto no Registrada")
        else:
            try:
                # Validate Description categoriaContacto
                result_categoria_Contacto = CategoriaContacto.objects.filter(desc_ctco = self.request.data.get("desc_ctco").upper().strip())
                if result_categoria_Contacto.count() > 0:
                    if result_categoria_Contacto[0].id != instance.id:
                        return message.ShowMessage("Descripcion de Categoria de Contacto ya Registrada con el ID:"+str(result_categoria_Contacto[0].id))

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.desc_ctco = request.data['desc_ctco'].upper().strip()
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"desc_ctco":instance.desc_ctco})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class CategoriaContactoDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = CategoriaContacto.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_ruta = CategoriaContacto.get_queryset().get(id=kwargs['id'])
            result_ruta.deleted = datetime.now()
            result_ruta.save()
            return message.DeleteMessage('Categoria de Contacto '+str(result_ruta.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Categoria de Contacto no Registrada")

# Drop Down
class CategoriaContactoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CategoriaContactoBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = CategoriaContacto.objects.all()
        show = self.request.query_params.get('show',None)
            
        if show =='true':
            return queryset.all()
        if show =='false' or show is None:
            return queryset.filter(deleted__isnull=True)
        