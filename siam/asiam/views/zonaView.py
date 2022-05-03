from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Zona
from asiam.serializers import ZonaSerializer
from asiam.paginations import SmallResultsSetPagination

class ZonaListView(generics.ListAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class ZonaCreateView(generics.CreateAPIView):
    serializer_class = ZonaSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class ZonaRetrieveView(generics.RetrieveAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.objects.all()
    lookup_field = 'id'

class ZonaUpdateView(generics.UpdateAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.objects.all()
    lookup_field = 'id'    

class ZonaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Zona.objects.all()
    lookup_field = 'id'
