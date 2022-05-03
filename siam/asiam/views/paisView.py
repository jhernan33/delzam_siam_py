from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Pais
from asiam.serializers import PaisSerializer
from asiam.paginations import SmallResultsSetPagination

class PaisListView(generics.ListAPIView):
    serializer_class = PaisSerializer
    permission_classes = ()
    queryset = Pais.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class PaisCreateView(generics.CreateAPIView):
    serializer_class = PaisSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class PaisRetrieveView(generics.RetrieveAPIView):
    serializer_class = PaisSerializer
    permission_classes = ()
    queryset = Pais.objects.all()
    lookup_field = 'id'

class PaisUpdateView(generics.UpdateAPIView):
    serializer_class = PaisSerializer
    permission_classes = ()
    queryset = Pais.objects.all()
    lookup_field = 'id'    

class PaisDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Pais.objects.all()
    lookup_field = 'id'

class PaisComboView(generics.ListAPIView):
    permission_classes = ()
    queryset = Pais.objects.all()
    lookup_field = 'id'
