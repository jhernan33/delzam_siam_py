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

from asiam.models import SubFamilia
from asiam.serializers import SubFamiliaSerializer
from asiam.paginations import SmallResultsSetPagination

class SubFamiliaListView(generics.ListAPIView):
    serializer_class = SubFamiliaSerializer
    permission_classes = []
    queryset = SubFamilia.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class SubFamiliaCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = SubFamiliaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SubFamiliaRetrieveView(generics.RetrieveAPIView):
    serializer_class = SubFamiliaSerializer
    permission_classes = []
    queryset = SubFamilia.objects.all()
    lookup_field = 'id'

class SubFamiliaUpdateView(generics.UpdateAPIView):
    serializer_class = SubFamiliaSerializer
    permission_classes = []
    queryset = SubFamilia.objects.all()
    lookup_field = 'id'    

class SubFamiliaDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = SubFamiliaSerializer
    queryset = SubFamilia.objects.all()
    lookup_field = 'id'
