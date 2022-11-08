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
from asiam.serializers import RutaSerializer, RutaBasicSerializer, RutaClienteSerializer
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
        try:
            name_route = self.request.data.get("nomb_ruta").upper().strip()
            code_zone = Zona.get_queryset().get(id=self.request.data.get("codi_zona")) 
            result_route = Ruta.objects.filter(nomb_ruta = name_route).filter(codi_zona_id = code_zone)
            # print(self.request.data.get("codi_zona"))
            if result_route.count() <= 0:
                try:
                    route = Ruta(
                        nomb_ruta = name_route,
                        codi_zona = code_zone,
                        created  = datetime.now()
                    )
                    route.save()
                    is_many = isinstance(self.request.data.get("sellers"),list)
                    if is_many:
                        for l in self.request.data.get("sellers"):
                            rutaDetalle  = RutaDetalleVendedor(codi_ruta_id = route.id,
                                codi_vend = Vendedor.get_queryset().get(id = l['codi_vend']),
                                created =  datetime.now(),
                                )
                            rutaDetalle.save()
                    return message.SaveMessage({"id":route.id,"nomb_ruta":route.nomb_ruta})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar La Ruta: "+str(e))
            elif result_route.count()>0:
                return message.ShowMessage({'information':name_route+' con la Zona '+str(code_zone.id),'message':"Ya Registrada"})
        except Zona.DoesNotExist:
            return message.NotFoundMessage("Id de Ruta no Registrado")

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
    queryset = Ruta.objects.all()
    lookup_field = 'id'

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
                # Save Detail Sellers
                is_many = isinstance(self.request.data.get("sellers"),list)
                if is_many:
                    RutaDetalleVendedor.objects.filter(codi_ruta_id = instance.id).delete()
                    for l in self.request.data.get("sellers"):
                        rutaDetalle  = RutaDetalleVendedor(codi_ruta_id = instance.id,
                            codi_vend = Vendedor.get_queryset().get(id = l['codi_vend']),
                            created =  datetime.now(),
                            )
                        rutaDetalle.save()

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
    serializer_class = RutaBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Ruta.objects.all()

        show = self.request.query_params.get('show',None)
        zone = self.request.query_params.get('zone',None)
        
        # Parameter Zone
        if zone:
            return queryset.filter(codi_zona = zone).filter(deleted__isnull=True)
            
        if show =='true':
            return queryset.all()
        if show =='false' or show is None:
            return queryset.filter(deleted__isnull=True)
        
class RutaClienteRetrieveView(generics.RetrieveAPIView):
    serializer_class = RutaClienteSerializer
    permission_classes = ()
    queryset = Ruta.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        customer = self.request.query_params.get('customer')

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