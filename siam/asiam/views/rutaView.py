from datetime import datetime, timezone
import re
from unittest import result
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from asiam.models import Ruta,Zona,Vendedor,RutaDetalleVendedor,Cliente
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
            name_rout = self.request.data.get("nomb_ruta").upper().strip()
            code_zone = Zona.get_queryset().get(id=self.request.data.get("codi_zona")) 
            porc_rout = self.request.data.get("porc_ruta")
            result_route = Ruta.objects.filter(nomb_ruta = name_rout).filter(codi_zona_id = code_zone)
            if result_route.count() <= 0:
                try:
                    route = Ruta(
                        nomb_ruta = name_rout,
                        codi_zona = code_zone,
                        porc_ruta = porc_rout,
                        created  = datetime.now()
                    )
                    route.save()
                    is_many = isinstance(self.request.data.get("sellers"),list)
                    if is_many:
                        for l in self.request.data.get("sellers"):
                            rutaDetalle  = RutaDetalleVendedor(
                                codi_ruta_id = route.id,
                                codi_vend = Vendedor.get_queryset().get(id = l['codi_vend']),
                                created =  datetime.now(),
                                )
                            rutaDetalle.save()
                    return message.SaveMessage({"id":route.id,"nomb_ruta":route.nomb_ruta})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar La Ruta: "+str(e))
            elif result_route.count()>0:
                return message.ShowMessage({'information':name_rout+' con la Zona '+str(code_zone.id),'message':"Ya Registrada"})
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
                _codi_zona = Zona.getInstanceZona(request.data['codi_zona'])
                # Validate Description Route
                result_route = Ruta.objects.filter(nomb_ruta = self.request.data.get("nomb_ruta").upper().strip()).filter(codi_zona = _codi_zona)
                if result_route.count() > 0:
                    if result_route[0].id != instance.id:
                        return message.ShowMessage("Descripcion de Ruta ya Registrada con el ID:"+str(result_route[0].id))

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = timezone.now()
                else:
                    isdeleted = None

                instance.nomb_ruta = str(request.data['nomb_ruta']).upper().strip()
                instance.porc_ruta = request.data['porc_ruta']
                instance.codi_zona = _codi_zona
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()

                # Save Detail Sellers
                is_many = isinstance(self.request.data.get("sellers"),list)
                if is_many:
                    # Search Routes
                    for l in self.request.data.get("sellers"):
                        _querysetSeller = RutaDetalleVendedor.objects.filter(codi_ruta_id = instance.id).filter(codi_vend_id = l['codi_vend'])
                        if _querysetSeller.count()>0:
                            # Check Id in use Cliente
                            Cliente.objects.filter(ruta_detalle_vendedor_cliente = _querysetSeller[0].id).update(updated = datetime.now())
                        else:
                            rutaDetalle  = RutaDetalleVendedor(codi_ruta_id = instance.id,
                                    codi_vend = Vendedor.get_queryset().get(id = l['codi_vend']),
                                    created =  datetime.now(),
                                    )
                            rutaDetalle.save()
                
                # Save Detail Customers
                is_many_Customer = isinstance(self.request.data.get("customers"),list)
                if is_many_Customer:     
                    for k in self.request.data.get("customers"):
                        Cliente.objects.filter(id = k['id']).update(posi_clie = k['posi_clie'],updated =  datetime.now())
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
        queryset = Ruta.objects.all().order_by('nomb_ruta')

        show = self.request.query_params.get('show',None)
        _only_zone = self.request.query_params.get('onlyzone',None)
        _report_zone = self.request.query_params.get('zone',None)
        
        if show =='true':
            queryset.all()
        if show =='false' or show is None:
            queryset.filter(deleted__isnull=True)
        
        # Parameter Only Zone
        if _only_zone:
            if isinstance(_only_zone,str):
                _zone = _only_zone
                # Convert Str to Tuple
                _result = tuple(map(int, _zone.split(',')))
                queryset = queryset.filter(codi_zona__in = _result).filter(deleted__isnull=True)
                return queryset
            
        # Parameter Zone Report Customer
        if _report_zone:
            if isinstance(_report_zone,str):
                _result = Ruta.getRouteFilterZone(_report_zone)
                queryset = queryset.filter(codi_zona__in = [_result]).filter(deleted__isnull=True)
        
        return queryset
            
        
        
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

