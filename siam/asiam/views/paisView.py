from multiprocessing import context
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Pais
from asiam.serializers import PaisSerializer, PaisBasicSerializer
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
    serializer_class = PaisBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.query_params.get('order') is not None:
            order = self.request.query_params.get('order')
            queryset = Pais.get_queryset().order_by(order)
        else:
            queryset = Pais.get_queryset().order_by('nomb_pais')
        return queryset