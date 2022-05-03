from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Vendedor
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
    serializer_class = VendedorSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

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
