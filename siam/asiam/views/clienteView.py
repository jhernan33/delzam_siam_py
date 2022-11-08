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

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser 
from rest_framework import status


from asiam.models import Cliente, Vendedor, Natural, Juridica, RutaDetalleVendedor
from asiam.serializers import ClienteSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

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
                        ,cred_clie                          = True if self.request.data.get("cred_clie").lower()=="true" else False
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
                    instance.cred_clie                          = True if self.request.data.get("cred_clie").lower()=="true" else False
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
