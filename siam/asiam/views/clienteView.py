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


from asiam.models import Cliente, Vendedor, Natural, Juridica, RutaDetalleVendedor, Ruta
from asiam.serializers import ClienteSerializer, ClienteReportSerializer, ClienteReportExportSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

from weasyprint import HTML
from django.http.request import QueryDict


class ClienteListView(generics.ListAPIView):
    serializer_class = ClienteSerializer
    permission_classes = ()
    queryset = Cliente.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    #filterset_fields = ['id','fein_clie','codi_ante','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','ruta_detalle_vendedor_cliente','ptor_clie']
    search_fields = ['id','fein_clie','codi_ante','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','ptor_clie','codi_natu__cedu_pena']
    ordering_fields = ['id','fein_clie','codi_ante','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','ptor_clie','codi_natu__cedu_pena']
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
                        ,location_clie                      = self.request.data.get("location_clie")
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
    serializer_class = ClienteSerializer    
    lookup_field = 'id'

    def get_queryset(self):
        estado_id = self.kwargs['id']
        queryset = Cliente.objects.all().order_by('-id')
        return queryset.filter(codi_esta_id = estado_id)    

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
            _seller_customer = _seller.split(',')
            #   Get Parameter Routes
            _route = self.request.query_params.get('route',None)
            if _route is not None:
                _route = _route.split(',')
                _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _route).filter(codi_vend__in = _seller_customer)
                queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail).order_by('id')
                return queryset
                

        # Check Parameter Route
        _route = self.request.query_params.get('route',None)
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
                queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail).order_by('id')
            return queryset
        
        # Check parameter zone
        zone = self.request.query_params.get('zone',None) 
        if zone is not None:
            _rutas = Ruta.getRouteFilterZone(zone)
            _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _rutas)
            queryset = Cliente.objects.filter(ruta_detalle_vendedor_cliente__in = _detail).order_by('id')
            return queryset
        
        # No Filter
        if queryset is None:   
            return Cliente.get_queryset().filter(deleted__isnull=True)
        elif queryset is not None:
            return queryset
        
""" 
*********************   Export Report to File (Pdf) *********************
"""
def ClienteExportFile(request):
    # serializer_class = ClienteReportExportSerializer
    # Get Values Request
    _zone = request.GET.get("zone",None)
    _route = request.GET.get("route",None)
    _seller = request.GET.get("seller",None)

    #   Create Queryset
    queryset = None   

    if type(_seller) == str:
        # Convert Str to List
        _seller_customer = _seller.split(',')

        #   Check Get Parameter Routes
        if _route is not None:
            _route = _route.split(',')
            _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _route).filter(codi_vend__in = _seller_customer)
            queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail).order_by('id').values()
            
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
            # queryset = serializer_class(queryset)
            _data = searchCustomer(_routeList)
            print(_data)
            
    # Check parameter zone
    if _zone is not None:
        _rutas = Ruta.getRouteFilterZone(_zone)
        _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _rutas)
        queryset = Cliente.objects.filter(ruta_detalle_vendedor_cliente__in = _detail).order_by('id').values()
    
    # No Filter
    if queryset is None:   
        queryset = Cliente.get_queryset().filter(deleted__isnull=True).values()
    
    # for value in queryset:
    #     print(value)

    context = {"data":queryset}
    html = render_to_string("customReport.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    # # font_config = FontConfiguration()
    HTML(string=html).write_pdf(response)

    return response

"""
Search Data Custom
"""
def searchCustomer(_routes):
    print(_routes)
    print(type(_routes))
    if isinstance(_routes,list):
        # Search Routes
        _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _routes).values("codi_vend","id")
        print(_detail)
        queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail[0]["codi_vend"]).order_by('id')
        print(queryset)
        # Search Seller
        
        # _result_natural = Natural.objects.filter(id = Vendedor.objects.filter(id = _detail[0]['codi_vend']).values('codi_natu'))
        # print(_result_natural)

    #     _objectCustomer = {}
    #     # for obj in _routes:
    #     #     # Search Routes
    #     #     _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = _routeList)
    #     #     queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail).order_by('id').values()
            
    #     #     _detail = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = obj)
    #     #     # print(_detail)
    #     #     # Search Custom
    #     #     queryset = Cliente.get_queryset().filter(ruta_detalle_vendedor_cliente__in = _detail).order_by('id').values()
    #     #     # print(queryset)
    #     #     # Search Seller
    #     #     _result_natural = Natural.objects.filter(id = Vendedor.objects.filter(id = _detail[0]['codi_vend']))
    #     #     _description = str(_result_natural[0].prno_pena[0]+"."+_result_natural[0].seno_pena[0]+"."+_result_natural[0].prap_pena[0]+"."+_result_natural[0].seap_pena[0]).strip().upper()
        
    #     #     # Create Object
    #     #     _objectCustomer.update({
    #     #         'id': queryset[0]['id'],
    #     #         'codi_ante': queryset[0]['codi_ante'],
    #     #         'description_customer': _description,
    #     #     })
    #     # print(_objectCustomer)
    #     # return _objectCustomer
    #         # # print(obj)
    #         # # _result_detail = RutaDetalleVendedor.objects.filter(codi_ruta = obj).values("codi_vend","id")
    #         # # print(_result_detail)
    #         # _result_seller = Vendedor.objects.filter(id = _detail[0]['codi_vend']).values('codi_natu')
    #         # # print(_result_seller)
    #         # _result_natural = Natural.objects.filter(id = _result_seller[0]['codi_natu'])
    #         # # print(_result_natural)
    #         # _description = str(_result_natural[0].prno_pena[0]+"."+_result_natural[0].seno_pena[0]+"."+_result_natural[0].prap_pena[0]+"."+_result_natural[0].seap_pena[0]).strip().upper()
    #         # # print(_description)

    #         # # Add Description for Natural or Juridica
    #         # # _description = Cliente.searchTypeCustomerId(instance.id)

    #         # # _resultClient = Cliente.objects.filter(id = _result_detail[0]['id']).values('id','codi_natu','codi_juri')
    #         # # print(_resultClient)
    #         # _descriptionCustomer = ""
    #         # # print("***************************")
    #         # for customer in queryset:
    #         #     # print(customer)
    #         #     if customer['codi_natu'] != 1:
    #         #         # print("Natural")
    #         #         _resultQuerySet = Natural.objects.filter(id = customer['codi_natu'])
    #         #         # print(_resultQuerySet)
    #         #         for natural in _resultQuerySet:
    #         #             #print(natural.cedu_pena)
    #         #             _descriptionCustomer = str(str(natural.cedu_pena)+" / "+natural.prno_pena+ ' '+natural.seno_pena+' '+natural.prap_pena+' '+ natural.seap_pena).strip().upper()+" (N)"
    #         #             # print(_descriptionCustomer)
    #         #     else:
    #         #         # print("Juridico")
    #         #         _resultQuerySet = Juridica.objects.filter(id = customer['codi_juri'])
    #         #         for juridica in _resultQuerySet:
    #         #             _descriptionCustomer = str(juridica.riff_peju+" / "+juridica.raso_peju).strip().upper()+" (J)"
    #         # print(_description)
    #         # print(_descriptionCustomer)
    #         # queryset['description_customer'] = str(_description)+" (Vend.) "+str(_descriptionCustomer)
    #         # # print(obj['description_customer'])