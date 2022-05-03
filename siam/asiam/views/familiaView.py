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

from asiam.models import Familia
from asiam.serializers import FamiliaSerializer
from asiam.paginations import SmallResultsSetPagination

class FamiliaListView(generics.ListAPIView):
    serializer_class = FamiliaSerializer
    permission_classes = []
    queryset = Familia.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class FamiliaCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = FamiliaSerializer    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created = datetime.now())

class FamiliaRetrieveView(generics.RetrieveAPIView):
    serializer_class = FamiliaSerializer
    permission_classes = []
    queryset = Familia.objects.all()
    lookup_field = 'id'

class FamiliaUpdateView(generics.UpdateAPIView):
    serializer_class = FamiliaSerializer
    permission_classes = ()
    queryset = Familia.objects.all()
    lookup_field = 'id'    

class FamiliaDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = FamiliaSerializer
    queryset = Familia.objects.all()
    lookup_field = 'id'
