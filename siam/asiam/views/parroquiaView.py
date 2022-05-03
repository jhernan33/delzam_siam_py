from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Parroquia
from asiam.serializers import ParroquiaSerializer
from asiam.paginations import SmallResultsSetPagination

class ParroquiaListView(generics.ListAPIView):
    serializer_class = ParroquiaSerializer
    permission_classes = ()
    queryset = Parroquia.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class ParroquiaCreateView(generics.CreateAPIView):
    serializer_class = ParroquiaSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class ParroquiaRetrieveView(generics.RetrieveAPIView):
    serializer_class = ParroquiaSerializer
    permission_classes = ()
    queryset = Parroquia.objects.all()
    lookup_field = 'id'

class ParroquiaUpdateView(generics.UpdateAPIView):
    serializer_class = ParroquiaSerializer
    permission_classes = ()
    queryset = Parroquia.objects.all()
    lookup_field = 'id'    

class ParroquiaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Parroquia.objects.all()
    lookup_field = 'id'
