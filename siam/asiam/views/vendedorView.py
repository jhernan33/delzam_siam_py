from datetime import datetime
import json
import os

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings

from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from asiam.models import Vendedor
from asiam.models import Natural,RutaDetalleVendedor, Ruta
from asiam.serializers import VendedorSerializer, VendedorBasicSerializer, NaturalSerializer, NaturalBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView

class VendedorListView(generics.ListAPIView):
    message = BaseMessage
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena']
    ordering_fields = ['id','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Vendedor.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return  queryset.filter(deleted__isnull=True)

    

class VendedorCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = VendedorSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        with transaction.atomic():
            try:
                result_seller = Vendedor.get_queryset().filter(codi_natu = self.request.data.get("codi_natu"))
                if result_seller.count() ==0:
                    result_natural = Natural.get_queryset().filter(id=self.request.data.get("codi_natu"))
                    if result_natural.count() >0:
                        enviroment = os.path.realpath(settings.WEBSERVER_SELLER)
                        ServiceImage = ServiceImageView()

                        json_photo_selller = None
                        if request.data['foto_vend'] is not None:
                            listImagesProv  = request.data['foto_vend']
                            json_photo_selller  = ServiceImage.saveImag(listImagesProv,enviroment)
                        vendedor = Vendedor(
                            fein_vend       = self.request.data.get("fein_vend")
                            ,codi_natu_id   = result_natural[0].id
                            ,foto_vend      = None if json_photo_selller is None else json_photo_selller
                            ,created        = datetime.now()
                        )
                        vendedor.save()
                        return message.SaveMessage({"id":vendedor.id})
                    else:
                        return message.NotFoundMessage("Id de Persona Natural no se encuentra Registrado")
                else:
                    return message.ShowMessage('Vendedor ya Registrado')
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Guardar el Vendedor: "+str(e))
            
                
class VendedorRetrieveView(generics.RetrieveAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Vendedor.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Vendedor no Registrado")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class VendedorUpdateView(generics.UpdateAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.objects.all()
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Vendedor no Registrado")
        else:
            with transaction.atomic():
                try:           
                    # Validate Id Natural
                    result_natural = Natural.validate_codi_natu(request.data['codi_natu'])
                    if result_natural == False:
                        return message.NotFoundMessage("Codigo de la Persona Natural no se encuentra Registrado")

                    # Validate Id Natural in Seller
                    result_seller = Vendedor.validate_codi_natu(request.data,instance.id)
                    if result_seller == False:
                        return message.NotFoundMessage("Codigo Natural Ya Asigando a otro Vendedor")

                    listImages = request.data['foto_vend']
                    enviroment = os.path.realpath(settings.WEBSERVER_SELLER)
                    ServiceImage = ServiceImageView()
                    json_images = ServiceImage.updateImage(listImages,enviroment)

                    Deleted = request.data['erased']
                    if Deleted:
                        isdeleted = datetime.now()
                    else:
                        result_natural = Natural.objects.get(id=request.data['codi_natu'])
                        result_natural.deleted = None
                        result_natural.save()
                        isdeleted = None

                    instance.codi_natu = Natural.objects.get(id = self.request.data.get("codi_natu"))
                    instance.foto_vend = json_images
                    instance.fein_vend = self.request.data.get("fein_vend")
                    instance.deleted = isdeleted
                    instance.updated = datetime.now()
                    instance.save()
                    return message.UpdateMessage({"id":instance.id})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))
    

class VendedorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id' 

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                vendedor = Vendedor.objects.get(pk=kwargs['id'])
                vendedor.deleted = datetime.now()
                vendedor.save()
                # Deleted Natural
                natural = Natural.objects.get(pk=vendedor.codi_natu_id)
                natural.deleted = datetime.now()
                natural.save()
                return message.DeleteMessage('Vendedor '+str(vendedor.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Vendedor no Registrado")
            
class VendedorComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = VendedorBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Vendedor.objects.all().order_by('-id')

        show = self.request.query_params.get('show',None)
        route = self.request.query_params.get('route',None)
        
        # Parameter route
        if route:
            return Vendedor.get_queryset().filter(id__in = RutaDetalleVendedor.get_queryset().filter(codi_ruta = route).values('codi_vend'))
            
        if show =='true':
            return queryset.all()
        if show =='false' or show is None:
            return queryset.filter(deleted__isnull=True)
