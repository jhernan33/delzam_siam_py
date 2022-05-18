from django.shortcuts import render
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Estado
from asiam.serializers import EstadoSerializer
from asiam.paginations import SmallResultsSetPagination

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http import HttpResponse

class EstadoListView(generics.ListAPIView):
    serializer_class = EstadoSerializer
    permission_classes = ()
    queryset = Estado.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class EstadoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = EstadoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EstadoRetrieveView(generics.RetrieveAPIView):
    serializer_class = EstadoSerializer
    permission_classes = ()
    queryset = Estado.objects.all()
    lookup_field = 'id'

class EstadoUpdateView(generics.UpdateAPIView):
    serializer_class = EstadoSerializer
    permission_classes = ()
    queryset = Estado.objects.all()
    lookup_field = 'id'    

class EstadoDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = EstadoSerializer    
    queryset = Estado.objects.all()
    lookup_field = 'id'

class EstadoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = EstadoSerializer    
    lookup_field = 'id'
    
    def get_queryset(self):
        pais_id = self.kwargs['id']
        queryset = Estado.objects.all()
        return queryset.filter(codi_pais_id = pais_id)