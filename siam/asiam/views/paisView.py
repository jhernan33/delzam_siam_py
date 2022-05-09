# from django.shortcuts import render
# from django.http import HttpResponse
# from django.http.response import JsonResponse

# from rest_framework import generics
# from rest_framework import filters as df
# from rest_framework.permissions import IsAuthenticated

from asiam.models import Pais
from asiam.serializers import PaisSerializer
from asiam.paginations import SmallResultsSetPagination

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from psycopg2 import Timestamp
from pytz import timezone

from rest_framework import status
from rest_framework import filters as df
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated



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
