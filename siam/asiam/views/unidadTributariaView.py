from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import UnidadTributaria
from asiam.serializers import UnidadTributariaSerializer
from asiam.paginations import SmallResultsSetPagination

class UnidadTributariaListView(generics.ListAPIView):
    serializer_class = UnidadTributariaSerializer
    permission_classes = ()
    queryset = UnidadTributaria.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class UnidadTributariaCreateView(generics.CreateAPIView):
    serializer_class = UnidadTributariaSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class UnidadTributariaRetrieveView(generics.RetrieveAPIView):
    serializer_class = UnidadTributariaSerializer
    permission_classes = ()
    queryset = UnidadTributaria.objects.all()
    lookup_field = 'id'

class UnidadTributariaUpdateView(generics.UpdateAPIView):
    serializer_class = UnidadTributariaSerializer
    permission_classes = ()
    queryset = UnidadTributaria.objects.all()
    lookup_field = 'id'    

class UnidadTributariaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = UnidadTributaria.objects.all()
    lookup_field = 'id'
