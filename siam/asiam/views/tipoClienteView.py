from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Tipocliente
from asiam.serializers import TipoClienteSerializer
from asiam.paginations import SmallResultsSetPagination

class TipoClienteListView(generics.ListAPIView):
    serializer_class = TipoClienteSerializer
    permission_classes = ()
    queryset = Tipocliente.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class TipoClienteCreateView(generics.CreateAPIView):
    serializer_class = TipoClienteSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class TipoClienteRetrieveView(generics.RetrieveAPIView):
    serializer_class = TipoClienteSerializer
    permission_classes = ()
    queryset = Tipocliente.objects.all()
    lookup_field = 'id'

class TipoClienteUpdateView(generics.UpdateAPIView):
    serializer_class = TipoClienteSerializer
    permission_classes = ()
    queryset = Tipocliente.objects.all()
    lookup_field = 'id'    

class TipoClienteDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Tipocliente.objects.all()
    lookup_field = 'id'
