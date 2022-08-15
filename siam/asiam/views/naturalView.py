from datetime import datetime
from django.shortcuts import render
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http import HttpResponse

from asiam.models import Natural
from asiam.serializers import NaturalSerializer, NaturalBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from django.core.exceptions import ObjectDoesNotExist

class NaturalListView(generics.ListAPIView):
    serializer_class = NaturalSerializer
    permission_classes = ()
    queryset = Natural.get_queryset()
    pagination_class = SmallResultsSetPagination
    filterset_fields = ['id','cedu_pena','prno_pena','seno_pena','prap_pena','seap_pena']
    search_fields = ['id','cedu_pena','prno_pena','seno_pena','prap_pena','seap_pena']
    ordering_fields = ['id','cedu_pena','prno_pena','seno_pena','prap_pena','seap_pena']

    def get_queryset(self):
        show = self.request.query_params.get('show',None)

        queryset = Natural.objects.all()
        if show =='true':
            queryset = queryset.filter(deleted__isnull=False)
        if show =='false' or show is None:
            queryset = queryset.filter(deleted__isnull=True)        

        field = self.request.query_params.get('field',None)
        value = self.request.query_params.get('value',None)
        if field is not None and value is not None:
            if field=='cedu_pena':
                queryset = queryset.filter(cedu_pena=value)
        return queryset


class NaturalCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = NaturalSerializer

    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_natural = Natural.get_queryset().filter(cedu_pena = str(self.request.data.get("cedu_pena")).strip())
            #result_rif     = Natural.get_queryset().filter(riff_pena = self.request.data.get("riff_pena").strip().upper())
            if result_natural.count() == 0:
                try:
                    natural = Natural(
                         cedu_pena      = str(self.request.data.get("cedu_pena")).strip().upper()
                        ,naci_pena      = str('' if self.request.data.get("naci_pena") is None else self.request.data.get("naci_pena")).strip().upper()
                        ,prno_pena      = str('' if self.request.data.get("prno_pena") is None else self.request.data.get("prno_pena")).strip().upper()
                        ,seno_pena      = str('' if self.request.data.get("seno_pena") is None else self.request.data.get("seno_pena")).strip().upper()
                        ,prap_pena      = str('' if self.request.data.get("prap_pena") is None else self.request.data.get("prap_pena")).strip().upper()
                        ,seap_pena      = str('' if self.request.data.get("seap_pena") is None else self.request.data.get("seap_pena")).strip().upper()
                        ,sexo_pena      = str('' if self.request.data.get("sexo_pena") is None else self.request.data.get("sexo_pena")).strip().upper()
                        ,edoc_pena      = str('' if self.request.data.get("edoc_pena") is None else self.request.data.get("edoc_pena")).strip().upper()
                        ,fena_pena      = self.request.data.get("fena_pena")
                        ,dire_pena      = str('' if self.request.data.get("dire_pena") is None else self.request.data.get("dire_pena")).strip().upper()
                        ,codi_ciud_id   = self.request.data.get("codi_ciud")
                        ,codi_sect_id   = self.request.data.get("codi_sect")
                        ,riff_pena      = str('' if self.request.data.get("riff_pena") is None else self.request.data.get("riff_pena")).strip().upper()
                        ,created        = datetime.now()
                    )
                    natural.save()
                    return message.SaveMessage('Registro Natural guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar la Persona Natural: "+str(e))
            elif result_natural.count()>0:
                return message.ShowMessage('Cedula ya Registrada')
        except Natural.DoesNotExist:
            return message.NotFoundMessage("Id de Natural no Registrado")
    

class NaturalRetrieveView(generics.RetrieveAPIView):
    serializer_class = NaturalSerializer
    permission_classes = ()
    queryset = Natural.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Natural.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)


class NaturalUpdateView(generics.UpdateAPIView):
    serializer_class = NaturalSerializer
    permission_classes = ()
    queryset = Natural.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Natural no Registrado")
        else:
            try:
                # Validate Cedu Pena
                # result_cedula = NaturalSerializer.validate_cedu_pena(request.data['cedu_pena'],)
                # if result_cedula == False:
                #     return message.NotFoundMessage("Cedula no es un Valor Valido de Persona Natural")

                # Validate Id Juridica
                result_riff = NaturalSerializer.validate_riff_pena(request.data['riff_pena'],request.data['cedu_pena'])
                if result_riff == True:
                    return message.ShowMessage("RIF no permitido, poruque se encuentra asignado a otra Persona Natural")

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.cedu_pena      = str(self.request.data.get("cedu_pena")).strip().upper()
                instance.naci_pena      = str('' if self.request.data.get("naci_pena") is None else self.request.data.get("naci_pena")).strip().upper()
                instance.prno_pena      = str('' if self.request.data.get("prno_pena") is None else self.request.data.get("prno_pena")).strip().upper()
                instance.seno_pena      = str('' if self.request.data.get("seno_pena") is None else self.request.data.get("seno_pena")).strip().upper()
                instance.prap_pena      = str('' if self.request.data.get("prap_pena") is None else self.request.data.get("prap_pena")).strip().upper()
                instance.seap_pena      = str('' if self.request.data.get("seap_pena") is None else self.request.data.get("seap_pena")).strip().upper()
                instance.sexo_pena      = str('' if self.request.data.get("sexo_pena") is None else self.request.data.get("sexo_pena")).strip().upper()
                instance.edoc_pena      = str('' if self.request.data.get("edoc_pena") is None else self.request.data.get("edoc_pena")).strip().upper()
                instance.fena_pena      = self.request.data.get("fena_pena")
                instance.dire_pena      = str('' if self.request.data.get("dire_pena") is None else self.request.data.get("dire_pena")).strip().upper()
                instance.codi_ciud_id   = self.request.data.get("codi_ciud")
                instance.codi_sect_id   = self.request.data.get("codi_sect")
                instance.riff_pena      = str('' if self.request.data.get("riff_pena") is None else self.request.data.get("riff_pena")).strip().upper()
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                return message.UpdateMessage(" La informacion de la Persona Natural con el Identificador: "+str(instance.id))
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class NaturalDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = NaturalSerializer
    lookup_field = 'id'
    queryset = Natural.get_queryset()

class NaturalFilterView(generics.ListCreateAPIView):
    permission_classes = ()
    serializer_class = NaturalSerializer 
    natural_separator = ','
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )
    
    def get_queryset(self):
        valor = self.request.query_params.get("valor", None)
        queryset = Natural.objects.raw("select id from ppal.natural(%s)",[valor])
        return queryset

class NaturalComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = NaturalBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Natural.get_queryset().order_by('-id')
        return queryset