from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import filters as df
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated

from asiam.models import Tesos
from asiam.serializers import TesosSerializer
from asiam.paginations import SmallResultsSetPagination

class TesosListView(generics.ListAPIView):
    serializer_class = TesosSerializer
    permission_classes = []
    queryset = Tesos.objects.all()
    #pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class TesosCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = TesosSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TesosRetrieveView(generics.RetrieveAPIView):
    serializer_class = TesosSerializer
    permission_classes = []
    queryset = Tesos.objects.all()
    lookup_field = 'id'

class TesosUpdateView(generics.UpdateAPIView):
    serializer_class = TesosSerializer
    permission_classes = []
    queryset = Tesos.objects.all()
    lookup_field = 'id'    

class TesosDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = TesosSerializer
    queryset = Tesos.objects.all()
    lookup_field = 'id'
