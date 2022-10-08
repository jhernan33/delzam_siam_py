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
from asiam.serializers import RutaDetalleVendedorSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class RutaDetalleVendedorListView(generics.ListAPIView):
    serializer_class = RutaDetalleVendedorSerializer
    permission_classes = ()
    queryset = RutaDetalleVendedor.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class RutaDetalleVendedorCreateView(generics.CreateAPIView):
    serializer_class = RutaDetalleVendedorSerializer
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
        try:
            result_ruta = RutaDetalleVendedor.get_queryset().filter(codi_ruta=self.request.data.get('codi_ruta')).filter(codi_vend=self.request.data.get('codi_vend'))
            if result_ruta.count()==0:
                with transaction.atomic():
                    try:
                        rutaDetalle  = RutaDetalleVendedor(codi_ruta_id = self.request.data.get('codi_ruta'),
                            codi_vend = Vendedor.get_queryset().get(id = self.request.data.get('codi_vend')),
                            created =  datetime.now(),
                            )
                        rutaDetalle.save()
                        return message.SaveMessage("Ruta Detalle Vendedor Guardada con Exito")
                    except Exception as e:
                        return message.ErrorMessage(str(e))
            else:
                return message.ShowMessage("Vendedor ya Asignado a la Ruta")    
        except Exception as e:
            return message.ErrorMessage("Error al Intentar Guardar la Ruta Detalle Vendedor "+str(e))
        # except Exception as e:
        #     return message.ErrorMessage("Error al Intentar Guardar Ruta "+str(e))
            

class RutaDetalleVendedorRetrieveView(generics.RetrieveAPIView):
    serializer_class = RutaDetalleVendedorSerializer
    permission_classes = ()
    queryset = RutaDetalleVendedor.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = RutaDetalleVendedor.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ruta Detalle Vendedor no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class RutaDetalleVendedorUpdateView(generics.UpdateAPIView):
    serializer_class = RutaDetalleVendedorSerializer
    permission_classes = ()
    queryset = RutaDetalleVendedor.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ruta no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Ruta")

class RutaDetalleVendedorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = RutaDetalleVendedor.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_ruta = RutaDetalleVendedor.get_queryset()
            result_ruta.deleted = datetime.now()
            result_ruta.save()
            return message.DeleteMessage('Ruta '+str(result_ruta.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Ruta no Registrada")

class RutaDetalleVendedorComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = RutaDetalleVendedorSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = RutaDetalleVendedor.get_queryset()
        return queryset