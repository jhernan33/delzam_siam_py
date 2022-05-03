from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import UnidadMedida
from asiam.serializers import UnidadMedidaSerializer
from asiam.paginations import SmallResultsSetPagination

class UnidadMedidaListView(generics.ListAPIView):
    serializer_class = UnidadMedidaSerializer
    permission_classes = ()
    queryset = UnidadMedida.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class UnidadMedidaCreateView(generics.CreateAPIView):
    serializer_class = UnidadMedidaSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class UnidadMedidaRetrieveView(generics.RetrieveAPIView):
    serializer_class = UnidadMedidaSerializer
    permission_classes = ()
    queryset = UnidadMedida.objects.all()
    lookup_field = 'id'

class UnidadMedidaUpdateView(generics.UpdateAPIView):
    serializer_class = UnidadMedidaSerializer
    permission_classes = ()
    queryset = UnidadMedida.objects.all()
    lookup_field = 'id'    

class UnidadMedidaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = UnidadMedida.objects.all()
    lookup_field = 'id'
