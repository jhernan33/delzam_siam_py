from datetime import datetime
from os import environ
import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http.response import JsonResponse
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser 
from rest_framework import status


from asiam.models import Pedido, PedidoDetalle, Cliente, Moneda, PedidoTipo, PedidoEstatus, Articulo
from asiam.serializers import PedidoSerializer, PedidoSerializer, ClienteComboSerializer, MonedaSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

from weasyprint import HTML
from django.http.request import QueryDict
from django.contrib.gis.geos import GEOSGeometry, Point


class PedidoListView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes =  [ IsAuthenticated ]
    queryset = Pedido.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi']
    ordering_fields = ['id','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Pedido.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        field = self.request.query_params.get('field',None)
        value = self.request.query_params.get('value',None)
        if field is not None and value is not None:
            if field=='codi_natu':
                queryset = queryset.filter(codi_natu=value)

        return queryset.filter(deleted__isnull=True)

class PedidoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = PedidoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Validate Customer Id
            result_customer = PedidoSerializer.validate_customer(request.data['customer'])
            if result_customer == False:
                return message.NotFoundMessage("Codigo de Cliente no Registrado")
                
            # Validate Id Currency
            result_currency = MonedaSerializer.check_Currency_Id(request.data['currency'])
            if result_currency == False:
                return message.NotFoundMessage("Codigo de Monenda no Registrado")
            
            # Check Details Orders
            if request.data['details'] is None:
                return message.NotFoundMessage("Items del Pedido es requerido")
            else:
                result_details = PedidoDetalle.checkDetails(self.request.data.get("details"))
                if result_details == False:
                    return message.NotFoundMessage("Items del Pedido son Incorrecto, verifique e Intente de Nuevo")
            
            enviroment = os.path.realpath(settings.WEBSERVER_ORDER)
            ServiceImage = ServiceImageView()
            json_foto_pedi = None
            if request.data['photo'] is not None:
                listImagesProv  = request.data['photo']
                json_foto_pedi  = ServiceImage.saveImag(listImagesProv,enviroment)
                with transaction.atomic():
                    order = Pedido(
                        codi_clie   = Cliente.get_queryset().get(id = self.request.data.get("customer")) 
                        ,fech_pedi  = Cliente.gettingTodaysDate() if self.request.data.get("date_created") is None else self.request.data.get("date_created")
                        ,mont_pedi  = self.request.data.get("amount")
                        ,desc_pedi  = self.request.data.get("discount")
                        ,tota_pedi  = self.request.data.get("total")
                        ,obse_pedi  = self.request.data.get("observations")
                        ,orig_pedi  = 'WebSite' if self.request.data.get("source") is None else self.request.data.get("source")
                        ,codi_mone  = 1 if self.request.data.get("currency") is None else Moneda.get_queryset().get(id =self.request.data.get("currency"))
                        ,codi_espe  = PedidoEstatus.get_queryset().get(id = 1)  if self.request.data.get("order_state") is None else PedidoEstatus.get_queryset().get(id = self.request.data.get("order_state")) 
                        ,codi_tipe  = 1 if self.request.data.get("order_type") is None else PedidoTipo.get_queryset().get(id = self.request.data.get("order_type")) 
                        ,foto_pedi  = None if json_foto_pedi is None else json_foto_pedi
                        ,created    = datetime.now()
                    )
                    order.save()
                    
                    # Save Details
                    if isinstance(self.request.data.get("details"),list):
                        _total = 0
                        for detail in self.request.data.get("details"):
                            # Guardar el Detalle
                            pedidoDetalle = PedidoDetalle(
                                codi_pedi = Pedido.get_queryset().get(id = order.id),
                                codi_arti = Articulo.get_queryset().get(id = detail['article']),
                                cant_pede = detail['quantity'],
                                prec_pede = detail['price'],
                                desc_pede = detail['discount'],
                                moto_pede = (detail['quantity'] * detail['price']) - detail['discount'],
                                created = Pedido.gettingTodaysDate(),
                            )
                            pedidoDetalle.save()
            return message.SaveMessage('Pedido guardado Exitosamente')
        except Exception as e:
            return message.ErrorMessage("Error al Intentar Guardar el Pedido: "+str(e))
            
class PedidoRetrieveView(generics.RetrieveAPIView):
    serializer_class = PedidoSerializer
    permission_classes = ()
    queryset = Pedido.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Pedido.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Pedido no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class PedidoUpdateView(generics.UpdateAPIView):
    serializer_class = PedidoSerializer
    permission_classes = ()
    queryset = Cliente.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Cliente no Registrado")
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
                
                # Validate Id Natural
                result_natural = PedidoSerializer.validate_codi_natu(request.data['codi_natu'],state_deleted)
                if result_natural == False:
                    return message.NotFoundMessage("Codi_Natu de Persona no Registrada")
                    
                # Validate Id Juridica
                result_juridica = PedidoSerializer.validate_codi_juri(request.data['codi_juri'],state_deleted)
                if result_juridica == False:
                    return message.NotFoundMessage("Codi_Juri de Persona Juridica no Registrada")
                
                # Validate Id Vendedor
                result_vendedor = PedidoSerializer.validate_codi_vend(request.data['codi_vend'])
                if result_vendedor == False:
                    return message.NotFoundMessage("Codi_Vend de Vendedor no Registrado")
                
                if result_vendedor and result_natural and result_juridica:
                    enviroment = os.path.realpath(settings.WEBSERVER_CUSTOMER)
                    ServiceImage = ServiceImageView()
                    json_foto_pedi = None

                    if request.data['foto_clie'] is not None:
                        listImagesProv  = request.data['foto_clie']
                        json_foto_pedi  = ServiceImage.updateImage(listImagesProv,enviroment)
                    
                    instance.ruta_detalle_vendedor_cliente      = RutaDetalleVendedor.get_queryset().get(id = self.request.data.get("codi_vend")) 
                    instance.codi_natu_id                       = self.request.data.get("codi_natu")
                    instance.codi_juri_id                       = self.request.data.get("codi_juri")
                    instance.fein_clie                          = self.request.data.get("fein_clie")
                    instance.codi_ante                          = str(self.request.data.get("codi_ante")).strip().upper()
                    instance.cred_clie                          = True if self.request.data.get("cred_clie").lower()=="t" else False
                    instance.mocr_clie                          = self.request.data.get("mocr_clie")
                    instance.plcr_clie                          = self.request.data.get("plcr_clie")
                    instance.prde_clie                          = self.request.data.get("prde_clie")
                    instance.prau_clie                          = self.request.data.get("prau_clie")
                    instance.foto_clie                          = None if json_foto_pedi is None else json_foto_pedi
                    instance.obse_clie                          = self.request.data.get("obse_clie")
                    instance.location_clie                      = self.request.data.get("location_clie")
                    instance.ptor_clie                          = self.request.data.get("ptor_clie")
                    instance.deleted                            = isdeleted
                    instance.updated                            = datetime.now()
                    instance.save()

                    # Check State Deleted
                    if state_deleted:
                        # Restore Natural Person
                        natural = Natural.objects.get(pk=instance.codi_natu_id)
                        natural.deleted = None
                        natural.save()
                        # Restore Legal Person
                        legal = Juridica.objects.get(pk=instance.codi_juri_id)
                        legal.deleted = None
                        legal.save()
                    return message.UpdateMessage({"id":instance.id,"mocr_clie":instance.mocr_clie,"plcr_clie":instance.plcr_clie})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class PedidoDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id' 

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                cliente = Cliente.objects.get(pk=kwargs['id'])
                cliente.deleted = datetime.now()
                cliente.save()
                # Deleted Natural
                natural = Pedido.objects.get(pk=cliente.codi_natu_id)
                natural.deleted = datetime.now()
                natural.save()
                # Deleted Legal
                if cliente.codi_juri_id != 1:
                    juridica = Juridica.objects.get(pk=cliente.codi_juri_id)
                    juridica.deleted = datetime.now()
                    juridica.save()

                return message.DeleteMessage('Cliente '+str(cliente.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Cliente no Registrado")
            
class PedidoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ClienteComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # estado_id = self.kwargs['id']
        queryset = Cliente.objects.all()
        list1 = list(queryset)
        return queryset