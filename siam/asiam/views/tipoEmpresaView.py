from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import TipoEmpresa
from asiam.serializers import TipoEmpresaSerializer
from asiam.paginations import SmallResultsSetPagination

class TipoEmpresaListView(generics.ListAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class TipoEmpresaCreateView(generics.CreateAPIView):
    serializer_class = TipoEmpresaSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class TipoEmpresaRetrieveView(generics.RetrieveAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    lookup_field = 'id'

class TipoEmpresaUpdateView(generics.UpdateAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    lookup_field = 'id'    

class TipoEmpresaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    lookup_field = 'id'
