from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.filters import SearchFilter, OrderingFilter

from asiam.models import Vendedor
from asiam.models import Natural
from asiam.serializers import VendedorSerializer, VendedorBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class VendedorListView(generics.ListAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['id','codi_natu_id']
    ordering_fields = ['id','codi_natu_id']
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
            with transaction.atomic():
                    try:
                        result_natural = Vendedor.objects.all().prefetch_related('codi_natu')
                        result_natural = result_natural.filter(codi_natu__cedu_pena = self.request.data.get("codi_natu"))

                        if result_natural.count() == 0:
                            try:
                                natural = Natural.objects.get(codi_natu = self.request.data.get("codi_natu"))
                                vendedor = Vendedor(
                                    fein_vend       = self.request.data.get("fein_vend")
                                    ,codi_natu_id   = natural.id
                                    ,created        = datetime.now()
                                )
                                vendedor.save()
                                return Response({'id':vendedor.id, 'feig_vend':vendedor.fein_vend},status=status.HTTP_201_CREATED)
                            except ObjectDoesNotExist:
                                natural = Natural(
                                    cedu_pena =  self.request.data.get("cedu_pena"),
                                    naci_pena =  self.request.data.get("naci_pena"),
                                    prno_pena =  self.request.data.get("prno_pena"),
                                    seno_pena =  self.request.data.get("seno_pena"),
                                    prap_pena =  self.request.data.get("prap_pena"),
                                    seap_pena =  self.request.data.get("seap_pena"),
                                    sexo_pena =  self.request.data.get("sexo_pena"),
                                    codi_ciud_id =  self.request.data.get("codi_ciud_id"),
                                    codi_sect_id =  self.request.data.get("codi_sect_id"),
                                    dire_pena =  self.request.data.get("dire_pena"),
                                    edoc_pena =  self.request.data.get("edoc_pena"),
                                    created =  datetime.now() 
                                )
                                natural.save()
                            
                                vendedor = Vendedor(
                                    fein_vend       = self.request.data.get("fein_vend")
                                    ,codi_natu_id   = natural.id
                                    ,created        = datetime.now()
                                )
                                vendedor.save()
                                return Response({'id':vendedor.id, 'feig_vend':vendedor.fein_vend},status=status.HTTP_201_CREATED)
                        else:
                            return Response({'data':'Cedula del Vendedor Ya Registrada','Numero de Cedula': self.request.data.get("cedu_pena")},status=status.HTTP_200_OK)
                    except Natural.DoesNotExist:
                        return Response({'data':'No se Encontro Natural'},status=status.HTTP_404_NOT_FOUND) 
                
class VendedorRetrieveView(generics.RetrieveAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.get_queryset()
    lookup_field = 'id'

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
    queryset = Vendedor.get_queryset()
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_update = Vendedor.get_queryset().get(id=kwargs['id'])
            result_update.fein_vend = self.request.data.get("fein_vend")
            result_update.updated = datetime.now()
            result_update.save()
            serialize = VendedorSerializer(result_update)
            return message.UpdateMessage(serialize.data) 
        except Exception as e:
            return message.NotFoundMessage("Id de Vendedor no Registrado")
    

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
        queryset = Vendedor.get_queryset().order_by('-id')
        return queryset