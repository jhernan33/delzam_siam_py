from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Ruta
from asiam.serializers import RutaSerializer
from asiam.paginations import SmallResultsSetPagination

class RutaListView(generics.ListAPIView):
    serializer_class = RutaSerializer
    permission_classes = ()
    queryset = Ruta.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class RutaCreateView(generics.CreateAPIView):
    serializer_class = RutaSerializer
    permission_classes = ()

class RutaRetrieveView(generics.RetrieveAPIView):
    serializer_class = RutaSerializer
    permission_classes = ()
    queryset = Ruta.objects.all()
    lookup_field = 'id'

class RutaUpdateView(generics.UpdateAPIView):
    serializer_class = RutaSerializer
    permission_classes = ()
    queryset = Ruta.objects.all()
    lookup_field = 'id'    

class RutaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Ruta.objects.all()
    lookup_field = 'id'
