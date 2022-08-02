from datetime import datetime
import re
from unittest import result
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from asiam.models import Ruta,Zona,Vendedor,RutaDetalleVendedor
from asiam.serializers import RutaSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage

class RutaListView(generics.ListAPIView):
    serializer_class = RutaSerializer
    permission_classes = ()
    queryset = Ruta.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ('id','nomb_ruta')
    ordering_fields = ('id', 'nomb_ruta')
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Ruta.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)

class RutaCreateView(generics.CreateAPIView):
    serializer_class = RutaSerializer
    # queryset = Ruta.get_queryset()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        message = BaseMessage
        # # many = isinstance(request.data,list)
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # serializer.save(created = datetime.now())
        # headers = self.get_success_headers(serializer.data)
        # return message.SaveMessage(serializer.data)

        # try:
        #     result_ruta = Ruta.get_queryset().filter(nomb_ruta = self.request.data.get("nomb_ruta"))
        #     if result_ruta.count()==0:
        #         with transaction.atomic():
        #             try:
        #                 ruta = Ruta(
        #                     nomb_ruta = self.request.data.get("nomb_ruta"),
        #                     codi_zona = Zona.get_queryset().get(id=self.request.data.get("codi_zona")) ,
        #                     created =  datetime.now(),
        #                 )
        #                 ruta.save()

        #                 # rutaDetalle  = RutaDetalleVendedor(codi_ruta_id = ruta.id,
        #                 #     codi_vend = Vendedor.get_queryset().get(id = self.request.data.get('codi_vend')),
        #                 #     created =  datetime.now(),
        #                 #     )
        #                 # rutaDetalle.save()
        #                 return message.SaveMessage("Ruta Guardada con Exito")
        #             except Exception as e:
        #                 return message.ErrorMessage(str(e))
                    
        # except Exception as e:
        #         # Verificar si la Ruta y Vendedor estan registrados en RutaDetalleVendedor
        #         rutaDetalle = RutaDetalleVendedor.get_queryset().filter(codi_ruta=self.request.data.get("codi_ruta")).filter(codi_vend = self.request.data.get("codi_vend"))
        #         if rutaDetalle.count()==0:
        #             rutaDetalle  = RutaDetalleVendedor(codi_ruta = self.request.data.get("codi_ruta"),
        #                 codi_vend = self.request.data.get('codi_vent'),
        #                 )
        #             rutaDetalle.save()
        #         return message.SaveMessage("Ruta Guardada con Exito")

        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ruta no Registrada")
        else:
            try:
                # Validate Description Route
                result_zone = Ruta.objects.filter(nomb_ruta = self.request.data.get("nomb_ruta").upper().strip())
                if result_zone.count() > 0:
                    if result_zone[0].id != instance.id:
                        return message.ShowMessage("Descripcion de Ruta ya Registrada con el ID:"+str(result_zone[0].id))

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.nomb_ruta = request.data['nomb_ruta'].upper().strip()
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                return message.UpdateMessage({"id":instance.id,"nomb_ruta":instance.desc_zona})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))
            

class RutaRetrieveView(generics.RetrieveAPIView):
    serializer_class = RutaSerializer
    permission_classes = ()
    queryset = Ruta.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Ruta.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ruta no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class RutaUpdateView(generics.UpdateAPIView):
    serializer_class = RutaSerializer
    permission_classes = ()
    queryset = Ruta.get_queryset()
    lookup_field = 'id'

    # def update(self, request, *args, **kwargs):
    #     message = BaseMessage
    #     try:
    #         instance = self.get_object()
    #     except Exception as e:
    #         return message.NotFoundMessage("Id de Ruta no Registrada")
    #     else:
    #         serializer = self.get_serializer(instance, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save(updated = datetime.now())
    #             return message.UpdateMessage(serializer.data)
    #         else:
    #             return message.ErrorMessage("Error al Intentar Actualizar Ruta")
    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ruta no Registrada")
        else:
            try:
                # Validate Description Route
                result_route = Ruta.objects.filter(nomb_ruta = self.request.data.get("nomb_ruta").upper().strip())
                if result_route.count() > 0:
                    if result_route[0].id != instance.id:
                        return message.ShowMessage("Descripcion de Ruta ya Registrada con el ID:"+str(result_route[0].id))

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.nomb_ruta = request.data['nomb_ruta'].upper().strip()
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                return message.UpdateMessage({"id":instance.id,"nomb_ruta":instance.nomb_ruta})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class RutaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Ruta.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_ruta = Ruta.get_queryset().get(id=kwargs['id'])
            result_ruta.deleted = datetime.now()
            result_ruta.save()
            return message.DeleteMessage('Ruta '+str(result_ruta.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Ruta no Registrada")

class RutaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = RutaSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Ruta.get_queryset().order_by('-id')
        return queryset