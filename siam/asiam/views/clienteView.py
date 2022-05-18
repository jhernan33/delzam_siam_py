import datetime
from django.shortcuts import render
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Cliente
from asiam.serializers import ClienteSerializer
from asiam.paginations import SmallResultsSetPagination

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http import HttpResponse

class ClienteListView(generics.ListAPIView):
    serializer_class = ClienteSerializer
    permission_classes = ()
    queryset = Cliente.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class ClienteCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = ClienteSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer.save(created = datetime.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            

class ClienteRetrieveView(generics.RetrieveAPIView):
    serializer_class = ClienteSerializer
    permission_classes = ()
    queryset = Cliente.objects.all()
    lookup_field = 'id'

class ClienteUpdateView(generics.UpdateAPIView):
    serializer_class = ClienteSerializer
    permission_classes = ()
    queryset = Cliente.objects.all()
    lookup_field = 'id'    

class ClienteDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = ClienteSerializer
    lookup_field = 'id'
    queryset = Cliente.objects.all()

class ClienteComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ClienteSerializer    
    lookup_field = 'id'

    def get_queryset(self):
        estado_id = self.kwargs['id']
        queryset = Cliente.objects.all().order_by('-id')
        return queryset.filter(codi_esta_id = estado_id)    
