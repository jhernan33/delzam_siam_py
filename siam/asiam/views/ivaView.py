from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Iva
from asiam.serializers import IvaSerializer
from asiam.paginations import SmallResultsSetPagination

class IvaListView(generics.ListAPIView):
    serializer_class = IvaSerializer
    permission_classes = ()
    queryset = Iva.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class IvaCreateView(generics.CreateAPIView):
    serializer_class = IvaSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class IvaRetrieveView(generics.RetrieveAPIView):
    serializer_class = IvaSerializer
    permission_classes = ()
    queryset = Iva.objects.all()
    lookup_field = 'id'

class IvaUpdateView(generics.UpdateAPIView):
    serializer_class = IvaSerializer
    permission_classes = ()
    queryset = Iva.objects.all()
    lookup_field = 'id'    

class IvaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Iva.objects.all()
    lookup_field = 'id'
