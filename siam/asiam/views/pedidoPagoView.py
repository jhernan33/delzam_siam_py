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

from asiam.models import PedidoPago, PedidoPagoDetalle, Cliente, Moneda, Articulo, Pedido
from asiam.serializers import PedidoPagoSerializer, PedidoPagoComboSerializer, MonedaSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

from weasyprint import HTML
from django.http.request import QueryDict
from django.contrib.gis.geos import GEOSGeometry, Point

class PedidoPagoListView(generics.ListAPIView):
    serializer_class = PedidoPagoSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoPago.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = [
        'id','codi_pedi','codi_esta','mont_pago','fech_pago','topa_pago'
        ]
    ordering_fields = ['id','codi_pedi','codi_esta','mont_pago','fech_pago','topa_pago']
    ordering = ['-id']

    def get_queryset(self):
        # Filter Except orders history
        queryset = PedidoPago.objects.all()

        # # Filter Pedido
        # order = self.request.query_params.get('order')
        # if order =='true':
        #     queryset = queryset.filter(codi_tipe=3)
        # else:
        #     queryset = queryset.exclude(codi_tipe=3)

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

class PedidoPagoCreateView(generics.CreateAPIView):
    permission_classes =  [IsAuthenticated]
    serializer_class = PedidoPagoSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            orderId = None
            stateId = None
            amount = None
            observations = None
            payDate = None
            totalPayment = None

            # Get User
            user_id = Token.objects.get(key= request.auth.key).user
            
            # Validate Order Id
            if 'order' in request.data:
                orderId = self.request.data.get("order")
                resultOrder = Pedido.checkOrder(orderId)
                if resultOrder == True:
                    return message.ShowMessage("Número de factura ya registrada al Cliente")
            
            
            # Validate Customer Id
            result_customer = PedidoPagoSerializer.validate_customer(request.data['customer'])
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
                return message.NotFoundMessage("Items del PedidoPago es requerido")
            else:
                result_details = PedidoPagoDetalle.checkDetails(self.request.data.get("details"))
                if result_details == False:
                    return message.NotFoundMessage("Items del PedidoPago son Incorrecto, verifique e Intente de Nuevo")
            
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
                order = PedidoPago(
                    codi_clie   = Cliente.get_queryset().get(id = self.request.data.get("customer")) 
                    ,fech_pedi  = Cliente.gettingTodaysDate() if self.request.data.get("date_created") is None else self.request.data.get("date_created")
                    #,mont_pedi  = self.request.data.get("amount")
                    #,desc_pedi  = self.request.data.get("discount")
                    #,tota_pedi  = self.request.data.get("total")
                    ,obse_pedi  = self.request.data.get("observations")
                    ,orig_pedi  = 'WebSite' if self.request.data.get("source") is None else self.request.data.get("source")
                    ,codi_mone  = Moneda.get_queryset().get(id = 1) if currency_id is None else Moneda.get_queryset().get(id = currency_id)
                    ,codi_espe  = PedidoPagoEstatus.get_queryset().get(id = 1)  if self.request.data.get("order_state") is None else PedidoPagoEstatus.get_queryset().get(id = self.request.data.get("order_state")) 
                    ,codi_tipe  = PedidoPagoTipo.get_queryset().get(id = 1)  if self.request.data.get("order_type") is None else PedidoPagoTipo.get_queryset().get(id = self.request.data.get("order_type")) 
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
                        PedidoPagoDetalle = PedidoPagoDetalle(
                            codi_pedi = PedidoPago.get_queryset().get(id = order.id),
                            codi_arti = Articulo.get_queryset().get(id = detail['article']),
                            cant_pede = detail_quantity,
                            prec_pede = detail_price,
                            desc_pede = detail_discount,
                            moto_pede = (detail_quantity * detail_price) - detail_discount,
                            created = datetime.now(),
                        )
                        PedidoPagoDetalle.save()
                        _amount = _amount + ((detail_quantity * detail_price) - detail_discount)

                # Update total in Order
                    PedidoPago.objects.filter(id = order.id).update(
                        mont_pedi = _amount
                        , desc_pedi = discount
                        , tota_pedi = _amount - (_amount * (discount / 100))
                        , updated = datetime.now()
                    )

                # Register Tracking
                orderTracking = PedidoPagoSeguimiento(
                    codi_pedi = PedidoPago.get_queryset().get(id = order.id),
                    codi_esta = PedidoPagoEstatus.get_queryset().get(id = 1),
                    codi_user = user_id,
                    fech_segu = datetime.now(),
                    created   = datetime.now(),
                    obse_segu = 'Creando el PedidoPago',
                )
                orderTracking.save()
            return message.SaveMessage({'message':'PedidoPago guardado exitosamente','id':order.id})
        except Exception as e:
            return message.ErrorMessage("Error al Intentar Guardar el PedidoPago: "+str(e))
            
class PedidoPagoRetrieveView(generics.RetrieveAPIView):
    permission_classes =  [IsAuthenticated]
    serializer_class = PedidoPagoSerializer
    queryset = PedidoPago.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = PedidoPago.objects.all()
        
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Pedido Pago no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class PedidoPagoUpdateView(generics.UpdateAPIView):
    serializer_class = PedidoPagoSerializer
    permission_classes = [IsAuthenticated]
    queryset = PedidoPago.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de PedidoPago no Registrado")
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
                    result_invoice = PedidoPagoSerializer.validate_customer_invoice_number(request.data['customer'],invoice_number)
                    if result_invoice == True:
                        return message.ShowMessage("Número de factura ya registrada al Cliente")
                
                # Validate Customer Id
                result_customer = PedidoPagoSerializer.validate_customer(request.data['customer'])
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
                    return message.NotFoundMessage("Items del PedidoPago es requerido")
                else:
                    result_details = PedidoPagoDetalle.checkDetails(self.request.data.get("details"))
                    if result_details == False:
                        return message.NotFoundMessage("Items del PedidoPago son Incorrecto, verifique e Intente de Nuevo")
                
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
                    instance.codi_espe  = PedidoPagoEstatus.get_queryset().get(id = 4)  if self.request.data.get("order_state") is None else PedidoPagoEstatus.get_queryset().get(id = self.request.data.get("order_state")) 
                    instance.codi_tipe  = 1 if self.request.data.get("order_type") is None else PedidoPagoTipo.get_queryset().get(id = self.request.data.get("order_type")) 
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
                        PedidoPagoDetalle.get_queryset().filter(codi_pedi = instance.id).delete()
                        for detail in self.request.data.get("details"):
                            detail_quantity = int(detail['quantity'])
                            detail_discount = float(detail['discount'])
                            detail_price = float(detail['price'])
                            # Save Order Detail
                            PedidoPagoDetalle = PedidoPagoDetalle(
                                codi_pedi = PedidoPago.get_queryset().get(id = instance.id),
                                codi_arti = Articulo.get_queryset().get(id = detail['article']),
                                cant_pede = detail_quantity,
                                prec_pede = detail_price,
                                desc_pede = detail_discount,
                                moto_pede = (detail_quantity * detail_price) - detail_discount,
                                created = datetime.now(),
                                updated = datetime.now(),
                            )
                            PedidoPagoDetalle.save()
                            _amount = _amount + ((detail_quantity * detail_price) - detail_discount)
                            _discount = _discount + detail_discount
                        # Update total in Order
                        PedidoPago.objects.filter(id = instance.id).update(
                            mont_pedi = _amount
                            , desc_pedi = _discount
                            , tota_pedi = _amount - (_amount * (_discount / 100))
                            , updated = datetime.now()
                        )
                    # Register Tracking
                    orderTracking = PedidoPagoSeguimiento(
                        codi_pedi = PedidoPago.get_queryset().get(id = instance.id),
                        codi_esta = PedidoPagoEstatus.get_queryset().get(id = self.request.data.get("order_status")),
                        codi_user = user_id,
                        fech_segu = datetime.now(),
                        created   = datetime.now(),
                        obse_segu = 'Actualizando el PedidoPago',
                    )
                    orderTracking.save()
                    return message.UpdateMessage("PedidoPago actualizado exitosamente")
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class PedidoPagoDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' 

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Instance Object
                orderState = PedidoPagoEstatus.get_queryset().get(id = 3)
                orderId =  PedidoPago.get_queryset().get(pk=kwargs['id'])
                order = orderId
                order.deleted = datetime.now()
                # Id Status Erased
                order.codi_espe = orderState
                order.save()

                # Deleted Detail
                updated_data = {
                    "deleted" : datetime.now()
                }
                result_order_detail = PedidoPagoDetalle.get_queryset().filter(codi_pedi = orderId).update(**updated_data)

                # Register Tracking
                orderTracking = PedidoPagoSeguimiento(
                    codi_pedi = orderId,
                    codi_esta = orderState,
                    codi_user = User.objects.get(id = request.user.id),
                    fech_segu = datetime.now(),
                    created   = datetime.now(),
                    obse_segu = 'Borrado del Registro',
                )
                orderTracking.save()

                return message.DeleteMessage('PedidoPago Anulado '+str(kwargs['id']))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de PedidoPago no Registrado")
            
class PedidoPagoComboView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoPagoComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = PedidoPago.get_queryset()
        list1 = list(queryset)
        return queryset
        message = BaseMessage
        return message.UnauthorizedMessage("para ver el Reporte")