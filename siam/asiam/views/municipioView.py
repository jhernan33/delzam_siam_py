from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Municipio
from asiam.serializers import MunicipioSerializer
from asiam.paginations import SmallResultsSetPagination

class MunicipioListView(generics.ListAPIView):
    serializer_class = MunicipioSerializer
    permission_classes = ()
    queryset = Municipio.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class MunicipioCreateView(generics.CreateAPIView):
    serializer_class = MunicipioSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class MunicipioRetrieveView(generics.RetrieveAPIView):
    serializer_class = MunicipioSerializer
    permission_classes = ()
    queryset = Municipio.objects.all()
    lookup_field = 'id'

class MunicipioUpdateView(generics.UpdateAPIView):
    serializer_class = MunicipioSerializer
    permission_classes = ()
    queryset = Municipio.objects.all()
    lookup_field = 'id'    

class MunicipioDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Municipio.objects.all()
    lookup_field = 'id'
