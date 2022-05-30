from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from asiam.models import TipoEmpresa
from asiam.serializers import TipoEmpresaSerializer
from asiam.paginations import SmallResultsSetPagination

class TipoEmpresaListView(generics.ListAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class TipoEmpresaCreateView(generics.CreateAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TipoEmpresaRetrieveView(generics.RetrieveAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    lookup_field = 'id'

class TipoEmpresaUpdateView(generics.UpdateAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    lookup_field = 'id'    

class TipoEmpresaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = TipoEmpresa.objects.all()
    lookup_field = 'id'
