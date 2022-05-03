import imp
from re import search
from urllib import request
import django
from django.http import HttpResponse
from django.shortcuts import render
from html5lib import serialize
from httplib2 import Response
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.paginator import Paginator

from asiam.models import Natural
from asiam.serializers import NaturalSerializer
from asiam.paginations import SmallResultsSetPagination

class NaturalListView(generics.ListAPIView):
    serializer_class = NaturalSerializer
    permission_classes = ()
    queryset = Natural.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class NaturalCreateView(generics.CreateAPIView):
    serializer_class = NaturalSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class NaturalRetrieveView(generics.RetrieveAPIView):
    serializer_class = NaturalSerializer
    permission_classes = ()
    queryset = Natural.objects.all()
    lookup_field = 'id'

class NaturalUpdateView(generics.UpdateAPIView):
    serializer_class = NaturalSerializer
    permission_classes = ()
    queryset = Natural.objects.all()
    lookup_field = 'id'    

class NaturalDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Natural.objects.all().delete
    lookup_field = 'id'

class NaturalFilterView(generics.ListCreateAPIView):
    permission_classes = ()
    serializer_class = NaturalSerializer 
    natural_separator = ','
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )
    def get_queryset(self):
        valor = self.request.query_params.get("valor", None)
        queryset = Natural.objects.raw("select id from ppal.natural(%s)",[valor])
        return queryset
