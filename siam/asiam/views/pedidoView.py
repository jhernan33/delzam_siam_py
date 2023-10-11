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
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from asiam.models import Pedido, PedidoDetalle, Cliente, Moneda, PedidoTipo, PedidoEstatus, Articulo, PedidoSeguimiento
from asiam.serializers import PedidoSerializer, PedidoSerializer, PedidoComboSerializer, MonedaSerializer
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
    permission_classes =  [ IsAuthenticated ]
    serializer_class = PedidoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Get User
            user_id = Token.objects.get(key= request.auth.key).user
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
                        ,codi_user  = 1 if self.request.data.get("user") is None else User.objects.get(id = self.request.data.get("user")) 
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
                                created = datetime.now(),
                            )
                            pedidoDetalle.save()
                    
                    # Register Tracking
                    orderTracking = PedidoSeguimiento(
                        codi_pedi = Pedido.get_queryset().get(id = order.id),
                        codi_esta = PedidoEstatus.get_queryset().get(id = 1),
                        codi_user = User.objects.get(id = request.user.id),
                        fech_segu = datetime.now(),
                        created   = datetime.now(),
                        obse_segu = 'Creando el Pedido',
                    )
                    orderTracking.save()
            return message.SaveMessage('Pedido guardado Exitosamente')
        except Exception as e:
            return message.ErrorMessage("Error al Intentar Guardar el Pedido: "+str(e))
            
class PedidoRetrieveView(generics.RetrieveAPIView):
    permission_classes =  [ IsAuthenticated ]
    serializer_class = PedidoSerializer
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
                # Instance Object
                orderState = PedidoEstatus.get_queryset().get(id = 3)
                orderId =  Pedido.get_queryset().get(pk=kwargs['id'])
                order = orderId
                order.deleted = datetime.now()
                # Id Status Erased
                order.codi_espe = orderState
                order.save()

                # Deleted Detail
                updated_data = {
                    "deleted" : datetime.now()
                }
                result_order_detail = PedidoDetalle.get_queryset().filter(codi_pedi = orderId).update(**updated_data)

                # Register Tracking
                orderTracking = PedidoSeguimiento(
                    codi_pedi = orderId,
                    codi_esta = orderState,
                    codi_user = User.objects.get(id = request.user.id),
                    fech_segu = datetime.now(),
                    created   = datetime.now(),
                    obse_segu = 'Borrado del Registro',
                )
                orderTracking.save()

                return message.DeleteMessage('Pedido Anulado '+str(kwargs['id']))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Pedido no Registrado")
            
class PedidoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = PedidoComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Pedido.get_queryset()
        list1 = list(queryset)
        return queryset
