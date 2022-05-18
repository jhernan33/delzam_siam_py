from datetime import datetime
import json
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

class VendedorListView(generics.ListAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class VendedorCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = VendedorSerializer
    
    def create(self, request, *args, **kwargs):
            with transaction.atomic():
                    result_natural = Vendedor.objects.all().prefetch_related('codi_natu')
                    result_natural = result_natural.filter(codi_natu__cedu_pena = self.request.data.get("cedu_pena"))
                    if result_natural.exists():
                        return Response({'data':'Cedula del Vendedor Ya Registrada','Numero de Cedula': self.request.data.get("cedu_pena")},status=status.HTTP_200_OK)
                    else:
                        # Verificar si existe la personal Natural
                        natural = Natural.objects.get(cedu_pena = self.request.data.get("cedu_pena"))
                        natural.naci_pena =  self.request.data.get("naci_pena")
                        natural.prno_pena =  self.request.data.get("prno_pena")
                        natural.seno_pena =  self.request.data.get("seno_pena")
                        natural.prap_pena =  self.request.data.get("prap_pena")
                        natural.seap_pena =  self.request.data.get("seap_pena")
                        natural.sexo_pena =  self.request.data.get("sexo_pena")
                        natural.codi_ciud_id =  self.request.data.get("codi_ciud_id")
                        natural.codi_sect_id =  self.request.data.get("codi_sect_id")
                        natural.dire_pena =  self.request.data.get("dire_pena")
                        natural.edoc_pena =  self.request.data.get("edoc_pena")
                        natural.created =  datetime.now()
                        natural.save()

                        vendedor = Vendedor(
                            fein_vend       = self.request.data.get("fein_vend")
                            ,codi_natu_id   = natural.id
                            ,created        = datetime.now()
                        )
                        vendedor.save()
                        return Response({'id':vendedor.id, 'feig_vend':vendedor.fein_vend},status=status.HTTP_201_CREATED)


class VendedorRetrieveView(generics.RetrieveAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.objects.all()
    lookup_field = 'id'

class VendedorUpdateView(generics.UpdateAPIView):
    serializer_class = VendedorSerializer
    permission_classes = ()
    queryset = Vendedor.objects.all()
    lookup_field = 'id'    

class VendedorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Vendedor.objects.all()
    lookup_field = 'id'
