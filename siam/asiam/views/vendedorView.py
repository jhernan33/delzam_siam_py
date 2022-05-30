from urllib.error import HTTPError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from genericpath import exists
import json
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from yaml import serialize
from django.db import transaction


from asiam.models import Vendedor
from asiam.models import Natural
from asiam.serializers import VendedorSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class VendedorListView(generics.ListAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class VendedorCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = VendedorSerializer
    
    def create(self, request, *args, **kwargs):
            with transaction.atomic():
                    try:
                        result_natural = Vendedor.objects.all().prefetch_related('codi_natu')
                        result_natural = result_natural.filter(codi_natu__cedu_pena = self.request.data.get("cedu_pena"))

                        if result_natural.count() == 0:
                            try:
                                natural = Natural.objects.get(cedu_pena = self.request.data.get("cedu_pena"))
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
            return message.NotFoundMessage("Id de Ciudad no Registrada")  
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
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Ciudad no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(fein_vend = self.request.data.get("fein_vend"),updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Actualizar Ciudad")
    

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
                #return Response({'result':'Registro Eliminado Exitosamente'},status=status.HTTP_200_OK)
                return message.DeleteMessage('Vendedor '+str(vendedor.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Vendedor no Registrado")
            
        
