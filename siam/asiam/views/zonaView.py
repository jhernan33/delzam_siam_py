from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Zona
from asiam.serializers import ZonaSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class ZonaListView(generics.ListAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class ZonaCreateView(generics.CreateAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class ZonaRetrieveView(generics.RetrieveAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.get_queryset()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Zona no Registrada")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class ZonaUpdateView(generics.UpdateAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.get_queryset()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Zona no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now())
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Zona")

class ZonaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_zona = Zona.get_queryset().get(id=kwargs['id'])
            result_zona.deleted = datetime.now()
            result_zona.save()
            return message.DeleteMessage('Zona '+str(result_zona.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Zona no Registrada")

class ZonaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ZonaSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Zona.get_queryset().order_by('-id')
        return queryset