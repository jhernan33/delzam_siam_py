from datetime import datetime
from os import environ
import os
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from yaml import serialize

from asiam.models import Juridica
from asiam.serializers import JuridicaSerializer, JuridicaBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from django.core.exceptions import ObjectDoesNotExist
from .serviceImageView import ServiceImageView

class JuridicaListView(generics.ListAPIView):
    serializer_class = JuridicaSerializer
    permission_classes = ()
    queryset = Juridica.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class JuridicaCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = JuridicaSerializer
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_juridica = Juridica.get_queryset().filter(riff_peju = self.request.data.get("riff_peju").strip().upper())
            result_raso = Juridica.get_queryset().filter(raso_peju = self.request.data.get("raso_peju").strip().upper())

            if result_juridica.count() == 0 and result_raso.count() ==0:
                enviroment = os.path.realpath(settings.WEBSERVER_LEGAL)
                ServiceImage = ServiceImageView()
                try:
                    if request.data['fori_peju'] is None:
                        listImagesRiff  = request.data['fori_peju']
                        json_foto_riff  = ServiceImage.saveImag(listImagesRiff,enviroment)

                    if request.data['folo_peju'] is None:
                        listImagesLocal = request.data['folo_peju']
                        json_foto_loca = ServiceImage.saveImag(listImagesLocal,enviroment)

                    juridica = Juridica(
                        riff_peju       = self.request.data.get("riff_peju").strip().upper()
                        ,raso_peju      = self.request.data.get("raso_peju").strip().upper()
                        ,dofi_peju      = self.request.data.get("dofi_peju").strip().upper()
                        ,ivaa_peju      = self.request.data.get("ivaa_peju")
                        ,islr_peju      = self.request.data.get("islr_peju")
                        ,desc_peju      = self.request.data.get("desc_peju").strip().upper()
                        ,fori_peju      = '' if json_foto_riff is None else json_foto_riff
                        ,folo_peju      = '' if json_foto_loca is None else json_foto_loca
                        ,pure_peju      = self.request.data.get("pure_peju").strip().upper()
                        ,fevi_peju      = self.request.data.get("fevi_peju")
                        ,codi_ciud_id   = self.request.data.get("codi_ciud_id")
                        ,codi_sect_id   = self.request.data.get("codi_sect_id")
                        ,codi_tiem_id   = self.request.data.get("codi_tiem_id")
                        ,created        = datetime.now()
                    )
                    juridica.save()
                    return message.SaveMessage('Registro Juridico guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar la Persona Juridica: "+str(e))
            elif result_juridica.count()>0:
                return message.ShowMessage('Rif ya Registrado')
            elif result_raso.count()>0:
                return message.ShowMessage('Razon Social ya Registrada')
        except Juridica.DoesNotExist:
            return message.NotFoundMessage("Id de Juridico no Registrado")

class JuridicaRetrieveView(generics.RetrieveAPIView):
    serializer_class = JuridicaSerializer
    permission_classes = ()
    queryset = Juridica.get_queryset()
    lookup_field = 'id'

class JuridicaUpdateView(generics.UpdateAPIView):
    serializer_class = JuridicaSerializer
    permission_classes = ()
    queryset = Juridica.get_queryset()
    lookup_field = 'id'    

class JuridicaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Juridica.get_queryset()
    lookup_field = 'id'

class JuridicaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = JuridicaBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Juridica.get_queryset().order_by('-id')
        return queryset