from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Accionista
from asiam.serializers import AccionistaSerializer
from asiam.paginations import SmallResultsSetPagination

class AccionistaListView(generics.ListAPIView):
    serializer_class = AccionistaSerializer
    permission_classes = ()
    queryset = Accionista.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class AccionistaCreateView(generics.CreateAPIView):
    serializer_class = AccionistaSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class AccionistaRetrieveView(generics.RetrieveAPIView):
    serializer_class = AccionistaSerializer
    permission_classes = ()
    queryset = Accionista.objects.all()
    lookup_field = 'id'

class AccionistaUpdateView(generics.UpdateAPIView):
    serializer_class = AccionistaSerializer
    permission_classes = ()
    queryset = Accionista.objects.all()
    lookup_field = 'id'    

class AccionistaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Accionista.objects.all()
    lookup_field = 'id'
