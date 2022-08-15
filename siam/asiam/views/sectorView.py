from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Sector
from asiam.serializers import SectorSerializer, SectorBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class SectorListView(generics.ListAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class SectorCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = SectorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class SectorRetrieveView(generics.RetrieveAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.get_queryset()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Sector no Registrado")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class SectorUpdateView(generics.UpdateAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Sector no Registrado")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Sector")

class SectorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Sector.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_sector = Sector.get_queryset().get(id=kwargs['id'])
            result_sector.deleted = datetime.now()
            result_sector.save()
            return message.DeleteMessage('Sector '+str(result_sector.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Sector no Registrado")

class SectorComboView(generics.ListAPIView):
    permission_classes = ()
    serializer_class = SectorBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.query_params.get('codi_ciud') == None:
            queryset = Sector.get_queryset().all()
        else:
            queryset = Sector.get_queryset().filter(codi_ciud = self.request.query_params.get('codi_ciud')).order_by('nomb_sect')
        return queryset