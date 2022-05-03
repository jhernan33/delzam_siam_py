from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Sucursal
from asiam.serializers import SucursalSerializer
from asiam.paginations import SmallResultsSetPagination

class SucursalListView(generics.ListAPIView):
    serializer_class = SucursalSerializer
    permission_classes = ()
    queryset = Sucursal.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class SucursalCreateView(generics.CreateAPIView):
    serializer_class = SucursalSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class SucursalRetrieveView(generics.RetrieveAPIView):
    serializer_class = SucursalSerializer
    permission_classes = ()
    queryset = Sucursal.objects.all()
    lookup_field = 'id'

class SucursalUpdateView(generics.UpdateAPIView):
    serializer_class = SucursalSerializer
    permission_classes = ()
    queryset = Sucursal.objects.all()
    lookup_field = 'id'    

class SucursalDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Sucursal.objects.all()
    lookup_field = 'id'
