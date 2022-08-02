from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from asiam.models import Zona
from asiam.serializers import ZonaSerializer, ZonaBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class ZonaListView(generics.ListAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ('id','desc_zona')
    ordering_fields = ('id', 'desc_zona')
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Zona.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)


class ZonaCreateView(generics.CreateAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            desc_zone = self.request.data.get("desc_zona").upper().strip()
            result_zone = Zona.objects.filter(desc_zona = desc_zone)

            if result_zone.count() <= 0:
                try:
                    zone = Zona(
                        desc_zona = desc_zone
                        ,created  = datetime.now()
                    )
                    zone.save()
                    return message.SaveMessage({"id":zone.id,"desc_zona":zone.desc_zona})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar La Zona: "+str(e))
            elif result_zone.count()>0:
                return message.ShowMessage('Descripcion de Zona ya Registrada')
        except Zona.DoesNotExist:
            return message.NotFoundMessage("Id de Zona no Registrado")


class ZonaRetrieveView(generics.RetrieveAPIView):
    serializer_class = ZonaSerializer
    permission_classes = ()
    queryset = Zona.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Zona.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

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
    queryset = Zona.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Zona no Registrada")
        else:
            try:
                # Validate Description Zone
                result_zone = Zona.objects.filter(desc_zona = self.request.data.get("desc_zona").upper().strip())
                if result_zone.count() > 0:
                    if result_zone[0].id != instance.id:
                        return message.ShowMessage("Descripcion de Zona ya Registrada con el ID:"+str(result_zone[0].id))

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.desc_zona = request.data['desc_zona'].upper().strip()
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                return message.UpdateMessage({"id":instance.id,"desc_zona":instance.desc_zona})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

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
    serializer_class = ZonaBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Zona.get_queryset().order_by('-id')
        return queryset