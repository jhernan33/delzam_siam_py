from datetime import datetime
from os import environ
import os
from rest_framework.decorators import api_view, permission_classes
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

from django.db.models import F
from asiam.models import Cliente, Vendedor, Natural, Juridica, RutaDetalleVendedor, Ruta, Contacto, Zona, Pedido
from asiam.serializers import ClienteSerializer, ClienteReportSerializer, ClienteReportExportSerializer, ClienteBasicSerializer, ClienteComboSerializer, ClienteBuscarSerializer, HistoryCustomerSerializer, HistoryCustomerReportSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView
from django.db.models import Prefetch, OuterRef

from weasyprint import HTML
from django.http.request import QueryDict
from django.contrib.gis.geos import GEOSGeometry, Point

class ClienteListView(generics.ListAPIView):
    serializer_class = ClienteSerializer
    permission_classes = ()
    queryset = Cliente.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    # Filtering by several fields
    search_fields = ['id','fein_clie','codi_ante','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','codi_juri__dofi_peju','ptor_clie','codi_natu__cedu_pena','codi_natu__razo_natu','codi_natu__codi_ciud__nomb_ciud','codi_natu__codi_sect__nomb_sect','codi_juri__codi_ciud__nomb_ciud','codi_juri__codi_sect__nomb_sect']
    ordering_fields = ['id','fein_clie','codi_ante','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','codi_juri__dofi_peju','ptor_clie','codi_natu__cedu_pena','codi_natu__razo_natu','codi_natu__codi_ciud__nomb_ciud','codi_natu__codi_sect__nomb_sect','codi_juri__codi_ciud__nomb_ciud','codi_juri__codi_sect__nomb_sect']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Cliente.objects.all()
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

class ClienteCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = ClienteSerializer
    
    def create(self, request, *args, **kwargs):
        DEFAULTPOINT = "POINT(1,1)"
        message = BaseMessage
        try:
            # Validate Id Natural
            result_natural = ClienteSerializer.validate_codi_natu(request.data['codi_natu'],False)
            if result_natural == False:
                return message.NotFoundMessage("Codi_Natu de Persona no Registrada")
                
            # Validate Id Juridica
            result_juridica = ClienteSerializer.validate_codi_juri(request.data['codi_juri'],False)
            if result_juridica == False:
                return message.NotFoundMessage("Codi_Juri de Persona Juridica no Registrada")
            
            # Validate Id Vendedor
            result_vendedor = ClienteSerializer.validate_codi_vend(request.data['codi_vend'])
            if result_vendedor == False:
                return message.NotFoundMessage("Codi_Vend de Vendedor no Registrado")

            if result_vendedor and result_natural and result_juridica:
                enviroment = os.path.realpath(settings.WEBSERVER_CUSTOMER)
                ServiceImage = ServiceImageView()
                try:
                    json_foto_clie = None
                    if request.data['foto_clie'] is not None:
                        listImagesProv  = request.data['foto_clie']
                        json_foto_clie  = ServiceImage.saveImag(listImagesProv,enviroment)
                    cliente = Cliente(
                        ruta_detalle_vendedor_cliente       = RutaDetalleVendedor.get_queryset().get(id = self.request.data.get("codi_vend")) 
                        ,codi_natu_id                       = self.request.data.get("codi_natu")
                        ,codi_juri_id                       = self.request.data.get("codi_juri")
                        ,fein_clie                          = self.request.data.get("fein_clie")
                        ,codi_ante                          = str(self.request.data.get("codi_ante")).strip().upper()
                        ,cred_clie                          = True if self.request.data.get("cred_clie").lower()=="t" else False
                        ,mocr_clie                          = self.request.data.get("mocr_clie")
                        ,plcr_clie                          = self.request.data.get("plcr_clie")
                        ,prde_clie                          = self.request.data.get("prde_clie")
                        ,prau_clie                          = self.request.data.get("prau_clie")
                        ,foto_clie                          = None if json_foto_clie is None else json_foto_clie
                        ,obse_clie                          = self.request.data.get("obse_clie")
                        ,location_clie                      = DEFAULTPOINT if self.request.data.get("location_clie") is None else self.request.data.get("location_clie")
                        ,ptor_clie                          = self.request.data.get("ptor_clie")
                        ,created                            = datetime.now()
                    )
                    cliente.save()
                    return message.SaveMessage('Cliente guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar el Cliente: "+str(e))
            elif result_vendedor.count()<=0:
                return message.NotFoundMessage('Registro Vendedor no Registrado')
            elif result_natural.count()<=0:
                return message.NotFoundMessage('Persona Natural no Registrada')
            elif result_juridica.count()<=0:
                return message.NotFoundMessage('Registro Juridico no Registrado')    
        except Cliente.DoesNotExist:
            return message.NotFoundMessage("Id de Cliente no Registrado")

class ClienteRetrieveView(generics.RetrieveAPIView):
    serializer_class = ClienteSerializer
    permission_classes = ()
    queryset = Cliente.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Cliente.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Cliente no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class ClienteUpdateView(generics.UpdateAPIView):
    serializer_class = ClienteSerializer
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
                result_natural = ClienteSerializer.validate_codi_natu(request.data['codi_natu'],state_deleted)
                if result_natural == False:
                    return message.NotFoundMessage("Codi_Natu de Persona no Registrada")
                    
                # Validate Id Juridica
                result_juridica = ClienteSerializer.validate_codi_juri(request.data['codi_juri'],state_deleted)
                if result_juridica == False:
                    return message.NotFoundMessage("Codi_Juri de Persona Juridica no Registrada")
                
                # Validate Id Vendedor
                result_vendedor = ClienteSerializer.validate_codi_vend(request.data['codi_vend'])
                if result_vendedor == False:
                    return message.NotFoundMessage("Codi_Vend de Vendedor no Registrado")
                
                if result_vendedor and result_natural and result_juridica:
                    enviroment = os.path.realpath(settings.WEBSERVER_CUSTOMER)
                    ServiceImage = ServiceImageView()
                    json_foto_clie = None

                    if request.data['foto_clie'] is not None:
                        listImagesProv  = request.data['foto_clie']
                        json_foto_clie  = ServiceImage.updateImage(listImagesProv,enviroment)
                    
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
                    instance.foto_clie                          = None if json_foto_clie is None else json_foto_clie
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

class ClienteDestroyView(generics.DestroyAPIView):
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
                if cliente.codi_natu_id != 1:
                    natural = Natural.objects.get(pk=cliente.codi_natu_id)
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

class ClienteComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ClienteComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # estado_id = self.kwargs['id']
        queryset = Cliente.objects.all()
        list1 = list(queryset)
        return queryset

"""
Report Customer filter Zone, Route, Seller
"""
class ClienteReportView(generics.ListAPIView):
    serializer_class = ClienteReportSerializer
    permission_classes = ()
    queryset = Cliente.get_queryset()
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        queryset = None
        
        # Check Parameter Seller
        _seller = self.request.query_params.get('seller',None)
        if type(_seller) == str:
            # Convert Str to List
            #_seller_customer = _seller.split(',')
            _seller_customer = tuple(map(int, _seller.split(',')))
            #   Get Parameter Routes
            _route = self.request.query_params.get('route',None)
            if _route is not None:
                #_route = _route.split(',')
                _route = tuple(map(int, _route.split(',')))

                # _detail = Ruta.get_queryset().filter(id in _route).values("nomb_ruta","codi_zona").select_related(RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _route).filter(codi_vend__in = _seller_customer).select_related(Ruta,"ruta__id"))
                _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _route).filter(codi_vend__in = _seller_customer)    # .select_related(Ruta,"ruta__id")
                queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail) # .order_by('codi_ante')
                return queryset
                

        # Check Parameter Route
        _route = self.request.query_params.get('route',None)
        if type(_route) == str and len(_route)>0:
            # Create List
            _routeList = []
            ocu_pri = 0
            # Check Count Ocurrences
            indexes = [i for i, c in enumerate(_route) if c ==',']
            if len(indexes) >0:
                # Iterate Indexes
                for x in indexes:
                    if ocu_pri == 0:
                        _routeList.append(int(_route[ocu_pri:x]))
                        ocu_pri = x
                    elif ocu_pri > 0:
                        _routeList.append(int(_route[ocu_pri+1:x]))
                        ocu_pri = x
                _routeList.append(int(_route[ocu_pri+1:len(_route)]))
            elif len(indexes) ==0:
                _routeList.append(int(_route[0:len(_route)]))

            if _routeList is not None:
                _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _routeList)
                queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail) # .order_by('codi_ante')
            return queryset
        
        # Check parameter zone
        zone = self.request.query_params.get('zone',None) 
        if zone is not None:
            # queryset = searchZone(zone)
            _rutas = Ruta.getRouteFilterZone(zone)
            _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _rutas)
            queryset = Cliente.objects.filter(ruta_detalle_vendedor_cliente__in = _detail) # .order_by('codi_ante')
            return queryset
        
        # No Filter
        if queryset is None:   
            return Cliente.get_queryset().filter(deleted__isnull=True)
        elif queryset is not None:
            return queryset
    
    '''
    Method Set Request
    '''
    def setRequestCustom(self,request):
        _zone = request.GET.get("zone",None)
        _route = request.GET.get("route",None)
        _seller = request.GET.get("seller",None)
        
        queryset = []
        queryset = Cliente.get_queryset()
        
        # Check Parameter Seller
        if type(_seller) == str:
            # Convert Str to List
            _seller_customer = _seller.split(',')
            #   Get Parameter Routes
            # _route = self.request.query_params.get('route',None)
            if _route is not None:
                _route = _route.split(',')
                _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _route).filter(codi_vend__in = _seller_customer)
                queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail) # .order_by('codi_ante')

                # Call method search Data Custom
                queryset = searchCustomNaturalJuridica(queryset)
                return queryset
                

        # Check Parameter Route
        if type(_route) == str:
            # Create List
            _routeList = []
            ocu_pri = 0
            # Check Count Ocurrences
            indexes = [i for i, c in enumerate(_route) if c ==',']
            if len(indexes) >0:
                # Iterate Indexes
                for x in indexes:
                    if ocu_pri == 0:
                        _routeList.append(int(_route[ocu_pri:x]))
                        ocu_pri = x
                    elif ocu_pri > 0:
                        _routeList.append(int(_route[ocu_pri+1:x]))
                        ocu_pri = x
                _routeList.append(int(_route[ocu_pri+1:len(_route)]))
            elif len(indexes) ==0:
                _routeList.append(int(_route[0:len(_route)]))

            if _routeList is not None:
                _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _routeList)
                queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail)
                # Call method search Data Custom
                queryset = searchCustomNaturalJuridica(queryset)
            return queryset
        
        # Check parameter zone
        if _zone is not None:
            # Call Filter Zonas
            _rutas = Ruta.getRouteFilterZone(_zone)
            _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _rutas)
            queryset = Cliente.objects.filter(ruta_detalle_vendedor_cliente__in = _detail) # .order_by('codi_ante')
            # Call method search Data Custom
            queryset = searchCustomNaturalJuridica(queryset)
            return queryset
        
        # No Filter
        if queryset is None:   
            return Cliente.get_queryset().filter(deleted__isnull=True)
        elif queryset is not None:
            return queryset
    
    """
        Get String Zones
    """
    def getZones(self,request):
        _zones = request.GET.get("zone",None)
        _allDescriptionZones = ""
        if _zones is not None:
            _allDescriptionZones = Zona.getZoneFilterArray(_zones)
        return _allDescriptionZones

'''
Find Customer by Code, Id, Natural, Juridic
'''
class ClienteBuscarView(generics.ListAPIView):
    serializer_class = ClienteBuscarSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cliente.get_queryset()
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    # Filtering by several fields
    search_fields = ['id','fein_clie','codi_ante','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','codi_juri__dofi_peju','ptor_clie','codi_natu__cedu_pena','codi_natu__razo_natu','codi_natu__codi_ciud__nomb_ciud','codi_natu__codi_sect__nomb_sect','codi_juri__codi_ciud__nomb_ciud','codi_juri__codi_sect__nomb_sect']
    ordering_fields = ['id','fein_clie','codi_ante','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','codi_juri__dofi_peju','ptor_clie','codi_natu__cedu_pena','codi_natu__razo_natu','codi_natu__codi_ciud__nomb_ciud','codi_natu__codi_sect__nomb_sect','codi_juri__codi_ciud__nomb_ciud','codi_juri__codi_sect__nomb_sect']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Cliente.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)

"""
    Search Filter Zone in Array
"""
def searchZone(_arrayZone):
    _queryset = Ruta.searchRouteFilterZone(_arrayZone)

"""
Search Data Custom
"""
def searchCustomNaturalJuridica(_queryset):
    
    for k in _queryset:
        # Add Description Seller
        _result_seller =  RutaDetalleVendedor.searchSeller(k.ruta_detalle_vendedor_cliente)
        _descriptionSeller = _result_seller

        # Add Description for Natural or Juridica
        _description = Cliente.searchTypeCustomerId(k.id)
        k.description_customer = _description+" (Vend.) "+_descriptionSeller

        # Add Contact for Customer c
        _contact = Contacto.search_contact(k.id)
        k.contact = _contact

        # Add Adress for Customer Contacto
        _address = Cliente.searchAddressCustomer(k.id)
        k.address = _address

        # Add Route and Zone
        _route = RutaDetalleVendedor.searchRouteZone(k.ruta_detalle_vendedor_cliente)
        k.route = _route[0].nomb_ruta
        k.zone = _route[0].codi_zona.desc_zona
        k.orde_zone = _route[0].codi_zona.orde_zona
        
        coordinates = k.location_clie
        a = GEOSGeometry(coordinates)
        b = a.ewkt
        coordinates = b.replace('SRID=4326;POINT ','').replace('(','').replace(')','')
        # Add Basic Coordinates
        k.coordinates = coordinates

    return _queryset

""" 
*********************   Export Report to File (Pdf) *********************
"""
def ClienteExportFile(request):
    # Instance Object
    objectReportView = ClienteReportView()
    result = objectReportView.setRequestCustom(request)

    _date = datetime.now().date()
    # Get All Zonas
    _zonas = objectReportView.getZones(request)
  
    # Create Context 
    context = {"data":result, "total":result.count, "Fecha":_date, "zonas":_zonas}
    html = render_to_string("customReport.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=report.pdf"
    
    # font_config = FontConfiguration()
    HTML(string=html).write_pdf(response)
    
    return response

'''
    Report History Customer
'''
class HistoryCustomer(generics.ListAPIView):
    serializer_class = HistoryCustomerSerializer
    permission_classes = ()
    # queryset = Cliente.objects.all()
    # pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        queryset = None

        queryset = self.filterCustomer(self)

        return queryset
    
    def filterCustomer(self,request):
        # Obtén los parámetros de búsqueda de la solicitud
        if self is not None:
            zone = self.request.query_params.get('zone')
            route = self.request.query_params.get('route')
            seller = self.request.query_params.get('seller')

        # Si estan definidos ambos `zone` y `seller`, se hace una búsqueda específica
        if zone and seller:
            routes = Ruta.getRouteFilterZone(zone)
            seller_obj = Vendedor.getSeller(seller)
            
            # Devuelve los resultados combinados, puedes cambiar el tipo de unión si es necesario            
            return searchHistoryCustomer(route = routes, seller=seller_obj) 
            #return searchHistoryCustomer(routes, "route") | searchHistoryCustomer(seller_obj, "seller")

        # Si están definidos tanto `route` como `seller`, se hace una búsqueda específica
        if route and seller:
            route_queryset = searchHistoryCustomer(route = route, seller=seller_obj)
            
            # Devuelve los resultados combinados, puedes cambiar el tipo de unión si es necesario
            return route_queryset

        # Si solo `zone` está definido, filtra por zona y busca en base a las rutas resultantes
        if zone and route is None:
            routes = Ruta.getRouteFilterZone(zone)
            return searchHistoryCustomer(route = routes)

        # Si solo `route` está definido, crea una lista de rutas y busca
        if route and zone:
            route_list = Ruta.createListRoute(route)
            if route_list:
                return searchHistoryCustomer(route = route_list)

        # Si solo `seller` está definido, busca por vendedor
        if seller:
            seller_obj = Vendedor.getSeller(seller)
            result = searchHistoryCustomer(seller=seller_obj)
            return result

        # Si no se definió ningún filtro, devuelve todas las rutas
        all_routes = Ruta.getAllRoute()
        return searchHistoryCustomer(all_routes, "route")
    
    def setRequestHistoryCustomer(self,request):
        _zone = request.GET.get("zone",None)
        _route = request.GET.get("route",None)
        _seller = request.GET.get("seller",None)

        resultQuery = HistoryCustomer.filterCustomer(zone=_zone,route=_route,seller=_seller)
        return resultQuery

def searchHistoryCustomer(**kwargs):
    queryset = None
    route = None
    seller = None 
    days = None

    for key, value in kwargs.items():
        if key == "route":
            route = value
        elif key == "seller":
            seller = value
        elif key == "Days":
            days = value
    
    if route and seller: 
        _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = route).filter(codi_vend__in = seller)

    if route and not seller:
        _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = route)

    if seller and not route:
        _detail = RutaDetalleVendedor.get_queryset().filter(codi_vend__in = seller)
    
    queryset = (Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail)
                .select_related("ruta_detalle_vendedor_cliente")
                .select_related("ruta_detalle_vendedor_cliente__codi_ruta")
                .select_related("ruta_detalle_vendedor_cliente__codi_ruta__codi_zona")
                .select_related("ruta_detalle_vendedor_cliente__codi_vend__codi_natu")
                .select_related("codi_natu")
                .select_related("codi_natu__codi_sect")
                .select_related("codi_natu__codi_ciud")
                .select_related("codi_juri")
                .select_related("codi_juri__codi_sect")
                .select_related("codi_juri__codi_ciud")
                .prefetch_related("order_customer_code").annotate(
                    Visit = Pedido.get_queryset().filter(
                        codi_clie = OuterRef('pk')).values(
                            "feim_pedi"
                            ).order_by("-feim_pedi")[:1],
                )
                .prefetch_related("contacto_cliente_codi_clie__codi_natu").annotate(
                    Contact_Natural = Contacto.get_queryset().filter(
                        codi_natu = OuterRef('codi_natu')).values(
                            "desc_cont"
                            ).order_by("desc_cont")[:1],   
                )
                .prefetch_related("contacto_cliente_codi_clie__codi_juri").annotate(
                    Contact_Legal = Contacto.get_queryset().filter(
                        codi_juri = OuterRef('codi_juri')).values(
                            "desc_cont"
                            ).order_by("desc_cont")[:1],   
                )
                .order_by('codi_ante').distinct("codi_ante")
                )
    return queryset

'''
Export Report History Customer
'''
def exportHistoryCustomer(request):
    zone = None
    route = None
    seller = None
    zone = request.GET.get('zone')
    route = request.GET.get('route')
    seller = request.GET.get('seller')
    days = request.GET.get('days')
    
    queryset = filterHistoryCustomer(zone,route,seller,days)
    for k in queryset:
        k.Days = days
    
    total = queryset.count()
    queryset = HistoryCustomerReportSerializer(queryset, many = True).data
    _date = datetime.now().date()
    # Create Context 
    context = {"data":queryset, "Fecha":_date, "total": total }
    return exportPdf(context)


def exportPdf(context):
    html = render_to_string("historyCustomerReport.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=report.pdf"
    
    # font_config = FontConfiguration()
    HTML(string=html).write_pdf(response)
    
    return response

def filterHistoryCustomer(zone = None, route=None, seller=None, days=None):

    # Si estan definidos ambos `zone` y `seller`, se hace una búsqueda específica
    if zone and seller:
        routes = Ruta.getRouteFilterZone(zone)
        seller_obj = Vendedor.getSeller(seller)

        # Devuelve los resultados combinados, puedes cambiar el tipo de unión si es necesario
        return searchHistoryCustomer(route = routes, seller=seller_obj, Days = days) 
        # return searchHistoryCustomer(routes, "route") | searchHistoryCustomer(seller_obj, "seller")

    # Si están definidos tanto `route` como `seller`, se hace una búsqueda específica
    if route and seller:
        route_queryset = searchHistoryCustomer(route = route, seller=seller_obj, Days = days)

        # Devuelve los resultados combinados, puedes cambiar el tipo de unión si es necesario
        return route_queryset

    # Si solo `zone` está definido, filtra por zona y busca en base a las rutas resultantes
    if zone and route is None:
        routes = Ruta.getRouteFilterZone(zone)
        return searchHistoryCustomer(route = routes, Days = days)

    # Si solo `route` está definido, crea una lista de rutas y busca
    if route and zone:
        route_list = Ruta.createListRoute(route)
        if route_list:
            return searchHistoryCustomer(route = route_list, Days = days)

    # Si solo `seller` está definido, busca por vendedor
    if seller:
        seller_obj = Vendedor.getSeller(seller)
        result = searchHistoryCustomer(seller=seller_obj, Days = days)
        return result

    # Si no se definió ningún filtro, devuelve todas las rutas
    all_routes = Ruta.getAllRoute()
    return searchHistoryCustomer(all_routes, "route", Days = days)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ClienteStatus(request):
    queryset = [
        {'id': 1, 'description': 'Disponible'},
        {'id': 2, 'description': 'Ocupado'},
        {'id': 3, 'description': 'Ambos'},
    ]
    return JsonResponse(queryset, safe=False)
