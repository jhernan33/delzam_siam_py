from django.shortcuts import render
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Ciudad
from asiam.serializers import CiudadSerializer
from asiam.paginations import SmallResultsSetPagination

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http import HttpResponse

class CiudadListView(generics.ListAPIView):
    serializer_class = CiudadSerializer
    permission_classes = ()
    queryset = Ciudad.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class CiudadCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = CiudadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CiudadRetrieveView(generics.RetrieveAPIView):
    serializer_class = CiudadSerializer
    permission_classes = ()
    queryset = Ciudad.objects.all()
    lookup_field = 'id'

class CiudadUpdateView(generics.UpdateAPIView):
    serializer_class = CiudadSerializer
    permission_classes = ()
    queryset = Ciudad.objects.all()
    lookup_field = 'id'    

class CiudadDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = CiudadSerializer    
    queryset = Ciudad.objects.all()
    lookup_field = 'id'


class CiudadComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CiudadSerializer    
    lookup_field = 'id'
    queryset = Ciudad.objects.all()
    
    def list(self, request, *args, **kwargs):
        pais_id = self.kwargs['id']
        paises = get_object_or_404(Ciudad,id=pais_id)
        Ciudads = Ciudad.objects.filter(codi_pais_id=pais_id)
        ser = CiudadSerializer(Ciudads,many=True).data
        return Response(ser, status=status.HTTP_200_OK)
    
