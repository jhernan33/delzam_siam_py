from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from asiam.models import Sector, Ciudad
from asiam.serializers import SectorSerializer, SectorBasicSerializer, CiudadSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class SectorListView(generics.ListAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','nomb_sect','codi_ciud__nomb_ciud']
    search_fields = ['id','nomb_sect','codi_ciud__nomb_ciud']
    ordering_fields = ['id','nomb_sect','codi_ciud__nomb_ciud']

    def get_queryset(self):
        show = self.request.query_params.get('show',None)

        queryset = Sector.objects.all()
        if show =='true':
            queryset = queryset.filter(deleted__isnull=False)
        if show =='false' or show is None:
            queryset = queryset.filter(deleted__isnull=True)        

        return queryset


class SectorCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = SectorSerializer

    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_sector = Sector.get_queryset().filter(nomb_sect = str(self.request.data.get("nomb_sect")).strip().upper())
            if result_sector.count() == 0:
                try:
                    sector = Sector(
                         nomb_sect      = str(self.request.data.get("nomb_sect")).strip().upper()
                        ,codi_ciud      = Ciudad.get_queryset().get(id = self.request.data.get("codi_ciud"))
                        ,created        = datetime.now()
                    )
                    sector.save()
                    return message.SaveMessage('Registro de Sector guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar la Sector: "+str(e))
            elif result_sector.count()>0:
                return message.ShowMessage('Nombre de Sector ya Registrado')
        except Sector.DoesNotExist:
            return message.NotFoundMessage("Id de Sector no Registrado")

class SectorRetrieveView(generics.RetrieveAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Sector.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

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
    queryset = Sector.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Sector no Registrado")
        else:
            try:
                # Validate Name Sector
                result_name_sector = SectorSerializer.validate_nomb_sect(str(request.data['nomb_sect']).upper().strip(),instance.id)
                if result_name_sector == True:
                    return message.ShowMessage("Nombre de Sector ya Registrado")

                # Validate Id City
                result_city = CiudadSerializer.validate_codi_cuid(request.data['codi_ciud'])
                if result_city == False:
                    return message.ShowMessage("Id de Ciudad No Regsistrado, en la Lista de Ciudad")

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.nomb_sect      = str('' if self.request.data.get("nomb_sect") is None else self.request.data.get("nomb_sect")).strip().upper()
                instance.codi_ciud      = Ciudad.get_queryset().get(id = self.request.data.get("codi_ciud"))
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                return message.UpdateMessage("Actualizado Exitosamente los Datos del Sector: "+str(instance.id))
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

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