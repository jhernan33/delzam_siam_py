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
from django.contrib.auth import get_user_model
from django.db.models import Q
import django_filters

from asiam.models import Pedido, PedidoDetalle, Cliente, Moneda, PedidoTipo, PedidoEstatus, Articulo, PedidoSeguimiento, PedidoMensaje
from asiam.serializers import PedidoSerializer, PedidoComboSerializer, MonedaSerializer,PedidoHistoricoSerializer, PedidoTipoSerializer, PedidoReportSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

from weasyprint import HTML
from django.http.request import QueryDict
from django.contrib.gis.geos import GEOSGeometry, Point

class PedidoListView(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pedido.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = [
        'id','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi'
        ,'obse_pedi','orig_pedi'
        ,'codi_clie__codi_natu__prno_pena','codi_clie__codi_natu__seno_pena','codi_clie__codi_natu__prap_pena'
        ,'codi_clie__codi_natu__seap_pena'
        ]
    ordering_fields = ['id','codi_clie','fech_pedi','feim_pedi','fede_pedi','feve_pedi','mont_pedi','desc_pedi','tota_pedi','obse_pedi','orig_pedi']
    ordering = ['-id']

    def get_queryset(self):
        # Filter Except orders history
        queryset = Pedido.objects.all()

        history = self.request.query_params.get('history')
        if history =='true':
            queryset = queryset.filter(codi_espe=7)
        else:
            queryset = queryset.exclude(codi_espe=7)

        show = self.request.query_params.get('show')
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        field = self.request.query_params.get('field',None)
        value = self.request.query_params.get('value',None)
        if field is not None and value is not None:
            if field=='state':
                queryset = queryset.filter(codi_espe=value)

        return queryset.filter(deleted__isnull=True)

class PedidoCreateView(generics.CreateAPIView):
    permission_classes =  [IsAuthenticated]
    serializer_class = PedidoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            invoice_number = None
            currency_id = None
            json_foto_pedi = None
            discount = 0
            _amount = 0

            # Get User
            user_id = Token.objects.get(key= request.auth.key).user
            
            # Validate Customer and Invoice Number
            if 'invoice_number' in request.data:
                invoice_number = str(self.request.data.get("invoice_number")).upper().strip()
                result_invoice = PedidoSerializer.validate_customer_invoice_number(request.data['customer'],invoice_number)
                if result_invoice == True:
                    return message.ShowMessage("Número de factura ya registrada al Cliente")
            
            
            # Validate Customer Id
            result_customer = PedidoSerializer.validate_customer(request.data['customer'])
            if result_customer == False:
                return message.NotFoundMessage("Codigo de Cliente no Registrado")
                
            # Validate Id Currency
            if 'currency' in request.data:
                currency_id = request.data['currency']
                result_currency = MonedaSerializer.check_Currency_Id(currency_id)
                if result_currency == False:
                    return message.NotFoundMessage("Codigo de Moneda no Registrado")
            
            # Check Details Orders
            if request.data['details'] is None:
                return message.NotFoundMessage("Items del Pedido es requerido")
            else:
                result_details = PedidoDetalle.checkDetails(self.request.data.get("details"))
                if result_details == False:
                    return message.NotFoundMessage("Items del Pedido son Incorrecto, verifique e Intente de Nuevo")
            
            enviroment = os.path.realpath(settings.WEBSERVER_ORDER)
            ServiceImage = ServiceImageView()
            
            if 'photo' in request.data:
                listImagesProv  = request.data['photo']
                json_foto_pedi  = ServiceImage.saveImag(listImagesProv,enviroment)
            
            # Velidate Discount
            if 'discount' in request.data:
                try:
                    discount = 0 if self.request.data.get("discount") is None else float(self.request.data.get("discount"))
                except ValueError:
                    discount = 0

            with transaction.atomic():
                order = Pedido(
                    codi_clie   = Cliente.get_queryset().get(id = self.request.data.get("customer")) 
                    ,fech_pedi  = Cliente.gettingTodaysDate() if self.request.data.get("date_created") is None else self.request.data.get("date_created")
                    #,mont_pedi  = self.request.data.get("amount")
                    #,desc_pedi  = self.request.data.get("discount")
                    #,tota_pedi  = self.request.data.get("total")
                    ,obse_pedi  = self.request.data.get("observations")
                    ,orig_pedi  = 'WebSite' if self.request.data.get("source") is None else self.request.data.get("source")
                    ,codi_mone  = Moneda.get_queryset().get(id = 1) if currency_id is None else Moneda.get_queryset().get(id = currency_id)
                    ,codi_espe  = PedidoEstatus.get_queryset().get(id = 1)  if self.request.data.get("order_state") is None else PedidoEstatus.get_queryset().get(id = self.request.data.get("order_state")) 
                    ,codi_tipe  = PedidoTipo.get_queryset().get(id = 1)  if self.request.data.get("order_type") is None else PedidoTipo.get_queryset().get(id = self.request.data.get("order_type")) 
                    ,mopo_pedi  = 20 if self.request.data.get("porcentage") is None else self.request.data.get("porcentage") 
                    ,foto_pedi  = None if json_foto_pedi is None else json_foto_pedi
                    ,nufa_pedi  = None if invoice_number is None else invoice_number
                    ,codi_user  = user_id
                    ,created    = datetime.now()
                )
                order.save()
                
                # Save Details
                if isinstance(self.request.data.get("details"),list):
                    for detail in self.request.data.get("details"):
                        detail_quantity = int(detail['quantity'])
                        detail_discount = float(detail['discount'])
                        detail_price = float(detail['price'])
                        # Guardar el Detalle
                        pedidoDetalle = PedidoDetalle(
                            codi_pedi = Pedido.get_queryset().get(id = order.id),
                            codi_arti = Articulo.get_queryset().get(id = detail['article']),
                            cant_pede = detail_quantity,
                            prec_pede = detail_price,
                            desc_pede = detail_discount,
                            moto_pede = (detail_quantity * detail_price) - detail_discount,
                            created = datetime.now(),
                        )
                        pedidoDetalle.save()
                        _amount = _amount + ((detail_quantity * detail_price) - detail_discount)

                # Update total in Order
                    Pedido.objects.filter(id = order.id).update(
                        mont_pedi = _amount
                        , desc_pedi = discount
                        , tota_pedi = _amount - (_amount * (discount / 100))
                        , updated = datetime.now()
                    )

                # Register Tracking
                orderTracking = PedidoSeguimiento(
                    codi_pedi = Pedido.get_queryset().get(id = order.id),
                    codi_esta = PedidoEstatus.get_queryset().get(id = 1),
                    codi_user = user_id,
                    fech_segu = datetime.now(),
                    created   = datetime.now(),
                    obse_segu = 'Creando el Pedido',
                )
                orderTracking.save()
            return message.SaveMessage({'message':'Pedido guardado exitosamente','id':order.id})
        except Exception as e:
            return message.ErrorMessage("Error al Intentar Guardar el Pedido: "+str(e))
            
class PedidoRetrieveView(generics.RetrieveAPIView):
    permission_classes =  [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Pedido no Registrado")
        else:
            try:
                invoice_number = None
                currency_id = None
                json_foto_pedi = None
                _discount = 0
                _amount = 0

                # Get User
                user_id = Token.objects.get(key= request.auth.key).user

                # Validate Customer and Invoice Number
                if 'invoice_number' in request.data:
                    invoice_number = str(self.request.data.get("invoice_number")).upper().strip()
                    result_invoice = PedidoSerializer.validate_customer_invoice_number(request.data['customer'],invoice_number)
                    if result_invoice == True:
                        return message.ShowMessage("Número de factura ya registrada al Cliente")
                
                # Validate Customer Id
                result_customer = PedidoSerializer.validate_customer(request.data['customer'])
                if result_customer == False:
                    return message.NotFoundMessage("Codigo de Cliente no Registrado")
                    
                # Validate Id Currency
                if 'currency' in request.data:
                    currency_id = request.data['currency']
                    result_currency = MonedaSerializer.check_Currency_Id(currency_id)
                    if result_currency == False:
                        return message.NotFoundMessage("Codigo de Monenda no Registrado")
                
                # Check Details Orders
                if request.data['details'] is None:
                    return message.NotFoundMessage("Items del Pedido es requerido")
                else:
                    result_details = PedidoDetalle.checkDetails(self.request.data.get("details"))
                    if result_details == False:
                        return message.NotFoundMessage("Items del Pedido son Incorrecto, verifique e Intente de Nuevo")
                
                # Velidate Discount
                if 'discount' in request.data:
                    try:
                        _discount = 0 if self.request.data.get("discount") is None else float(self.request.data.get("discount"))
                    except ValueError:
                        _discount = 0

                # State Deleted
                state_deleted = None
                if instance.deleted:
                    state_deleted = True
                
                Deleted = request.data['erased']
                if Deleted:                    
                    isdeleted = datetime.now()
                else:    
                    isdeleted = None

                enviroment = os.path.realpath(settings.WEBSERVER_ORDER)
                ServiceImage = ServiceImageView()
                json_foto_pedi = None
                if request.data['photo'] is not None:
                    listImagesProv  = request.data['photo']
                    json_foto_pedi  = ServiceImage.saveImag(listImagesProv,enviroment)

                # Update Order
                with transaction.atomic():
                    instance.codi_clie  = Cliente.get_queryset().get(id = self.request.data.get("customer")) 
                    instance.fech_pedi  = Cliente.gettingTodaysDate() if self.request.data.get("date_created") is None else self.request.data.get("date_created")
                    # instance.mont_pedi  = self.request.data.get("amount")
                    # instance.desc_pedi  = self.request.data.get("discount")
                    # instance.tota_pedi  = self.request.data.get("total")
                    instance.obse_pedi  = self.request.data.get("observations")
                    instance.orig_pedi  = 'WebSite' if self.request.data.get("source") is None else self.request.data.get("source")
                    instance.codi_mone  = Moneda.get_queryset().get(id = 1) if currency_id is None else Moneda.get_queryset().get(id = currency_id)
                    instance.codi_espe  = PedidoEstatus.get_queryset().get(id = 4)  if self.request.data.get("order_state") is None else PedidoEstatus.get_queryset().get(id = self.request.data.get("order_state")) 
                    instance.codi_tipe  = 1 if self.request.data.get("order_type") is None else PedidoTipo.get_queryset().get(id = self.request.data.get("order_type")) 
                    instance.mopo_pedi  = 20 if self.request.data.get("porcentage") is None else self.request.data.get("porcentage") 
                    instance.foto_pedi  = None if json_foto_pedi is None else json_foto_pedi
                    instance.nufa_pedi  = None if invoice_number is None else invoice_number
                    instance.codi_user  = user_id
                    instance.deleted    = isdeleted
                    instance.updated    = datetime.now()
                    instance.save()

                    # Save Details
                    if isinstance(self.request.data.get("details"),list):
                        _total = 0
                        # Delete Items Order Detail
                        PedidoDetalle.get_queryset().filter(codi_pedi = instance.id).delete()
                        for detail in self.request.data.get("details"):
                            detail_quantity = int(detail['quantity'])
                            detail_discount = float(detail['discount'])
                            detail_price = float(detail['price'])
                            # Save Order Detail
                            pedidoDetalle = PedidoDetalle(
                                codi_pedi = Pedido.get_queryset().get(id = instance.id),
                                codi_arti = Articulo.get_queryset().get(id = detail['article']),
                                cant_pede = detail_quantity,
                                prec_pede = detail_price,
                                desc_pede = detail_discount,
                                moto_pede = (detail_quantity * detail_price) - detail_discount,
                                created = datetime.now(),
                                updated = datetime.now(),
                            )
                            pedidoDetalle.save()
                            _amount = _amount + ((detail_quantity * detail_price) - detail_discount)
                            _discount = _discount + detail_discount
                        # Update total in Order
                        Pedido.objects.filter(id = instance.id).update(
                            mont_pedi = _amount
                            , desc_pedi = _discount
                            , tota_pedi = _amount - (_amount * (_discount / 100))
                            , updated = datetime.now()
                        )
                    # Register Tracking
                    orderTracking = PedidoSeguimiento(
                        codi_pedi = Pedido.get_queryset().get(id = instance.id),
                        codi_esta = PedidoEstatus.get_queryset().get(id = self.request.data.get("order_status")),
                        codi_user = user_id,
                        fech_segu = datetime.now(),
                        created   = datetime.now(),
                        obse_segu = 'Actualizando el Pedido',
                    )
                    orderTracking.save()
                    return message.UpdateMessage("Pedido actualizado exitosamente")
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class PedidoDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Pedido.get_queryset()
        list1 = list(queryset)
        return queryset

class PedidoHistorico(generics.CreateAPIView):
    permission_classes =  [IsAuthenticated]
    serializer_class = PedidoHistoricoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            # Get User

            user_id = Token.objects.get(key= request.auth.key).user
            # Validate Customer and Invoice Number
            result_invoice = PedidoSerializer.validate_customer_invoice_number(request.data['customer'],request.data['invoice_number'],None)
            if result_invoice == True:
                return message.ShowMessage("Número de factura ya registrada al Cliente")
            
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
            
            amount = float(self.request.data.get("total"))
            invoice_number = str(self.request.data.get("invoice_number")).upper().strip()
            with transaction.atomic():
                order = Pedido(
                    codi_clie   = Cliente.get_queryset().get(id = self.request.data.get("customer")) 
                    ,feim_pedi  = Cliente.gettingTodaysDate() if self.request.data.get("date_printer") is None else self.request.data.get("date_printer")
                    ,mont_pedi  = None if self.request.data.get("amount") is None else self.request.data.get("amount")
                    ,desc_pedi  = None if self.request.data.get("discount") is None else self.request.data.get("discount")
                    ,tota_pedi  = self.request.data.get("total") - (self.request.data.get("total")*(self.request.data.get("porcentage")/100))
                    ,obse_pedi  = None if self.request.data.get("observations") is None else self.request.data.get("observations")
                    ,orig_pedi  = 'WebSite' if self.request.data.get("source") is None else self.request.data.get("source")
                    ,codi_mone  = 1 if self.request.data.get("currency") is None else Moneda.get_queryset().get(id =self.request.data.get("currency"))
                    ,codi_espe  = PedidoEstatus.get_queryset().get(id = 7)  if self.request.data.get("order_state") is None else PedidoEstatus.get_queryset().get(id = self.request.data.get("order_state")) 
                    ,codi_tipe  = 2 if self.request.data.get("order_type") is None else PedidoTipo.get_queryset().get(id = self.request.data.get("order_type")) 
                    ,foto_pedi  = None if json_foto_pedi is None else json_foto_pedi
                    ,nufa_pedi  = None if invoice_number is None else invoice_number
                    ,mopo_pedi  = 20 if self.request.data.get("porcentage") is None else self.request.data.get("porcentage")
                    ,codi_user  = user_id
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
                            codi_arti = Articulo.objects.get(id = detail['article']),
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
                    codi_esta = PedidoEstatus.get_queryset().get(id = 7),
                    codi_user = user_id,
                    fech_segu = datetime.now(),
                    created   = datetime.now(),
                    obse_segu = 'Registrando el Pedido Historico en fecha de: '+ datetime.now().strftime('%Y-%m-%d, %H:%M:%S') + ' por el Usuario: '+ str(self.request.user),
                )
                orderTracking.save()
            return message.SaveMessage('Pedido guardado Exitosamente')
        except Exception as e:
            return message.ErrorMessage("Error al Intentar Guardar el Pedido: "+str(e))

class PedidoHistoricoUpdateView(generics.UpdateAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Pedido Historico no Registrado")
        else:
            try:
                # Get User
                user_id = Token.objects.get(key= request.auth.key).user
                
                # Validate Customer Id
                result_customer = PedidoSerializer.validate_customer(request.data['customer'])
                if result_customer == False:
                    return message.NotFoundMessage("Codigo de Cliente no Registrado")
                
                # Validate Customer and Invoice Number
                result_invoice = PedidoSerializer.validate_customer_invoice_number(request.data['customer'],request.data['invoice_number'],instance.id)
                if result_invoice == True:
                    return message.ShowMessage("Número de factura ya registrada al Cliente")
                
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
                
                # State Deleted
                state_deleted = None
                if instance.deleted:
                    state_deleted = True
                
                Deleted = request.data['erased']
                if Deleted:                    
                    isdeleted = datetime.now()
                else:    
                    isdeleted = None
                
                enviroment = os.path.realpath(settings.WEBSERVER_ORDER)
                ServiceImage = ServiceImageView()
                json_foto_pedi = None
                if request.data['photo'] is not None:
                    listImagesProv  = request.data['photo']
                    json_foto_pedi  = ServiceImage.saveImag(listImagesProv,enviroment)

                invoice_number = str(self.request.data.get("invoice_number")).upper().strip()
                with transaction.atomic():
                
                    instance.codi_clie  = Cliente.get_queryset().get(id = self.request.data.get("customer")) 
                    instance.feim_pedi  = Cliente.gettingTodaysDate() if self.request.data.get("date_printer") is None else self.request.data.get("date_printer")
                    instance.mont_pedi  = self.request.data.get("amount")
                    instance.desc_pedi  = None if self.request.data.get("discount") is None else self.request.data.get("discount")
                    instance.tota_pedi  = self.request.data.get("total") - (self.request.data.get("total")*(self.request.data.get("porcentage")/100))
                    instance.obse_pedi  = None if self.request.data.get("observations") is None else self.request.data.get("observations")
                    instance.orig_pedi  = 'WebSite' if self.request.data.get("source") is None else self.request.data.get("source")
                    instance.codi_mone  = 1 if self.request.data.get("currency") is None else Moneda.get_queryset().get(id =self.request.data.get("currency"))
                    instance.codi_espe  = PedidoEstatus.get_queryset().get(id = 7)  if self.request.data.get("order_state") is None else PedidoEstatus.get_queryset().get(id = self.request.data.get("order_state")) 
                    instance.codi_tipe  = 2 if self.request.data.get("order_type") is None else PedidoTipo.get_queryset().get(id = self.request.data.get("order_type")) 
                    instance.foto_pedi  = None if json_foto_pedi is None else json_foto_pedi
                    instance.nufa_pedi  = None if invoice_number is None else invoice_number
                    instance.mopo_pedi  = 20 if self.request.data.get("porcentage") is None else self.request.data.get("porcentage")
                    instance.codi_user  = user_id
                    instance.deleted    = isdeleted
                    instance.updated    = datetime.now()
                    instance.save()

                    # Save Details
                    if isinstance(self.request.data.get("details"),list):
                        _total = 0
                        # Delete Items Order Detail
                        PedidoDetalle.get_queryset().filter(codi_pedi = instance.id).delete()
                        for detail in self.request.data.get("details"):
                            # Save Order Detail
                            pedidoDetalle = PedidoDetalle(
                                codi_pedi = Pedido.get_queryset().get(id = instance.id),
                                codi_arti = Articulo.get_queryset().get(id = detail['article']),
                                cant_pede = detail['quantity'],
                                prec_pede = detail['price'],
                                desc_pede = detail['discount'],
                                moto_pede = (detail['quantity'] * detail['price']) - detail['discount'],
                                created = datetime.now(),
                                updated = datetime.now(),
                            )
                            pedidoDetalle.save()
                    # Register Tracking
                    orderTracking = PedidoSeguimiento(
                        codi_pedi = Pedido.get_queryset().get(id = instance.id),
                        codi_esta = PedidoEstatus.get_queryset().get(id = 7),
                        codi_user = user_id,
                        fech_segu = datetime.now(),
                        created   = datetime.now(),
                        obse_segu = 'Actualizando el Pedido Historico',
                    )
                    orderTracking.save()
                    return message.UpdateMessage({"id":instance.id})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar: "+str(e))

# class PedidoSearchView(django_filters.FilterSet):
#     q = django_filters.CharFilter(method='my_custom_filter', label="Search")

#     # serializer_class = PedidoSerializer
#     # permission_classes = [IsAuthenticated]
#     # queryset = Pedido.get_queryset()
#     # pagination_class = SmallResultsSetPagination
#     # ordering = ['-id']
#     class Meta:
#         model = Cliente
#         fields = ['q']

#     def my_custom_filter(self, queryset, name, value):
#         result = queryset.filter(
#             Q(loc__icontains=value) |
#             Q(loc_codi_ante__icontains=value) | 
#             Q(loc_codi_natu__prno_pena__icontains=value) | 
#             Q(loc_codi_natu__seno_pena__icontains=value) | 
#             Q(loc_codi_natu__prap_pena__icontains=value) | 
#             Q(loc_codi_natu__seap_pena__icontains=value) | 
#             Q(loc_codi_juri__riff_peju__icontains=value) |
#             Q(loc_codi_juri__raso_peju__icontains=value) |
#             Q(loc_codi_juri__dofi_peju__icontains=value) |
#             Q(loc_codi_natu__cedu_pena__icontains=value) |
#             Q(loc_codi_natu__razo_natu__icontains=value) |
#             Q(loc_codi_natu__codi_ciud__nomb_ciud__icontains=value) |
#             Q(loc_codi_natu__codi_sect__nomb_sect__icontains=value) |
#             Q(loc_codi_juri__codi_ciud__nomb_ciud__icontains=value) |
#             Q(loc_codi_juri__codi_sect__nomb_sect__icontains=value)
#         )
#         # print("Result====",result)
#         return result

    # def get_queryset(self):
    #     queryset = None

    #     _search = self.request.query_params.get("search",None)
    #     if _search is not None:
    #         _result_customer = Cliente.get_queryset().filter()
    #         queryset = Pedido.filter(codi_clie__in = _result_customer)
    #     return queryset

'''
    Change Order Type
'''
class PedidoUpdateStatusView(generics.UpdateAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Pedido no Registrado")
        else:
            try:
                state_id = None

                # Get User
                user_id = Token.objects.get(key= request.auth.key).user

                # Validate Customer and Invoice Number
                if 'state' in request.data:
                    state_id = self.request.data.get("state")
                    result_state = PedidoTipoSerializer.validate_codi_tipe(state_id)
                    if result_state == False:
                        return message.NotFoundMessage("Id de Estatus no Registrado")
                    
                    state_id = PedidoTipo.getInstanceOrderType(state_id)
                # Update Order
                with transaction.atomic():
                    instance.codi_tipe  = state_id
                    instance.codi_user  = user_id
                    instance.updated    = datetime.now()
                    instance.save()

                    # Register Tracking
                    orderTracking = PedidoSeguimiento(
                        codi_pedi = Pedido.getInstanceOrder(instance.id),
                        codi_esta = PedidoEstatus.getInstanceOrderState(4),
                        codi_user = user_id,
                        fech_segu = datetime.now(),
                        created   = datetime.now(),
                        obse_segu = 'Cambiando el Estatus de Pedido al de: ',
                    )
                    orderTracking.save()
                    return message.UpdateMessage("Estatus actualizado exitosamente")
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

def PedidoReport(request):
    if request.headers.get('Authorization') is not None:
        show = request.GET.get('show',None)
        _id = request.GET.get('id',None)
        if _id is not None:
            message = ''
            customer_all = None
            queryset = Pedido.getOrderFilterById(_id,show)
            customer_all = queryset.get('customer_all')
            customer_address = queryset.get('customer_address')
            customer_phone = queryset.get('customer_phone')
            invoice_number = queryset.get('invoice_number')
            total_amount = queryset.get('total_amount')
            result_message = PedidoMensaje.filterByCodiTipe(queryset.get('type_order_id'))
            if result_message.count()> 0 :
                for k in result_message:
                    message = k

        # result = queryset
        _date = datetime.now().date()
        # Create Context 
        context = {
                "data":queryset
                , "invoice_number": invoice_number
                , "customer":customer_all
                , 'customer_address':customer_address
                , 'customer_phone': customer_phone
                , "total":total_amount
                , "fecha":_date
                , "message": message
                }
        html = render_to_string("invoice.html", context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; report.pdf"

        # font_config = FontConfiguration()
        HTML(string=html).write_pdf(response)

        return response
    else:
        message = BaseMessage
        return message.UnauthorizedMessage("para ver el Reporte")