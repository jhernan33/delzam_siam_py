from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import TipoEmpresa
from asiam.serializers import TipoEmpresaSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class TipoEmpresaListView(generics.ListAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.get_queryset()
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
    queryset = TipoEmpresa.get_queryset()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Tipo de Empresa no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class TipoEmpresaUpdateView(generics.UpdateAPIView):
    serializer_class = TipoEmpresaSerializer
    permission_classes = ()
    queryset = TipoEmpresa.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Tipo de Empresa no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return Response({"message":"Error al Actualizar"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TipoEmpresaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    # queryset = TipoEmpresa.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = TipoEmpresa.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Ciudad '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Ciudad no Registrada")

class TipoEmpresaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = TipoEmpresaSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = TipoEmpresa.get_queryset().order_by('-id')
        return queryset

