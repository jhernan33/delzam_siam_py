from datetime import datetime
from os import environ
import os
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from yaml import serialize

from asiam.models import Juridica, Ciudad, Sector, TipoEmpresa, Contacto,Cliente
from asiam.serializers import JuridicaSerializer, JuridicaBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage
from django.core.exceptions import ObjectDoesNotExist
from .serviceImageView import ServiceImageView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Exists, OuterRef


class JuridicaListView(generics.ListAPIView):
    serializer_class = JuridicaSerializer
    permission_classes = ()
    queryset = Juridica.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','riff_peju','raso_peju','desc_peju','dofi_peju','desc_peju','pure_peju']
    search_fields = ('id','riff_peju','raso_peju','desc_peju','dofi_peju','desc_peju','pure_peju')
    ordering_fields = ('id','riff_peju','raso_peju','desc_peju','dofi_peju','desc_peju','pure_peju')

    def get_queryset(self):
        show = self.request.query_params.get('show',None)

        queryset = Juridica.objects.all().order_by('-id')
        if show =='true':
            queryset = queryset.filter(deleted__isnull=False)
        if show =='false' or show is None:
            queryset = queryset.filter(deleted__isnull=True)        

        field = self.request.query_params.get('field',None)
        value = self.request.query_params.get('value',None)
        if field is not None and value is not None:
            if field=='riff_peju':
                queryset = queryset.filter(riff_peju=value)
        return queryset

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
                json_foto_riff = None
                json_foto_loca = None
                try:
                    listImagesRiff  = request.data['fori_peju']
                    json_foto_riff  = ServiceImage.saveImag(listImagesRiff,enviroment)

                    listImagesLocal = request.data['folo_peju']
                    json_foto_loca = ServiceImage.saveImag(listImagesLocal,enviroment)

                    juridica = Juridica(
                        riff_peju       = str(self.request.data.get("riff_peju")).strip().upper()
                        ,raso_peju      = str(self.request.data.get("raso_peju")).strip().upper()
                        ,dofi_peju      = str(self.request.data.get("dofi_peju")).strip().upper()
                        ,ivaa_peju      = self.request.data.get("ivaa_peju")
                        ,islr_peju      = self.request.data.get("islr_peju")
                        ,desc_peju      = str(self.request.data.get("desc_peju")).strip().upper()
                        ,fori_peju      = None if json_foto_riff is None else json_foto_riff
                        ,folo_peju      = None if json_foto_loca is None else json_foto_loca
                        ,pure_peju      = str(self.request.data.get("pure_peju")).strip().upper()
                        ,fevi_peju      = self.request.data.get("fevi_peju")
                        ,codi_ciud_id   = self.request.data.get("codi_ciud")
                        ,codi_sect_id   = self.request.data.get("codi_sect")
                        ,codi_tiem_id   = self.request.data.get("codi_tiem")
                        ,created        = datetime.now()
                    )
                    juridica.save()

                    #   Check Save Contacts
                    if isinstance(self.request.data.get("contacts"),list):
                        for contact in self.request.data.get("contacts"):
                            result_contact = Contacto.check_contact(contact['codi_cont'],contact['codi_grou'])
                            if result_contact == False:
                                contact = Contacto(
                                    desc_cont      = contact['codi_cont']
                                    ,codi_grco_id   = contact['codi_grou']
                                    ,codi_juri_id   = juridica.id
                                    ,created        = datetime.now()
                                )
                                contact.save()
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

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Juridica.objects.all()

        if show =='true' and self.kwargs['id']!=1:
            queryset = queryset.filter(deleted__isnull=False)
            return queryset
        
        return queryset.filter(deleted__isnull=True)
    
    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Juridico no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class JuridicaUpdateView(generics.UpdateAPIView):
    serializer_class = JuridicaSerializer
    permission_classes = ()
    queryset = Juridica.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Juridica no Registrado")
        else:
            enviroment = os.path.realpath(settings.WEBSERVER_LEGAL)
            ServiceImage = ServiceImageView()
            json_foto_riff = None
            json_foto_loca = None
            try:
                #if request.data['fori_peju'] is None:
                listImagesRiff  = request.data['fori_peju']
                json_foto_riff  = ServiceImage.updateImage(listImagesRiff,enviroment)

                #if request.data['folo_peju'] is None:
                listImagesLocal = request.data['folo_peju']
                json_foto_loca = ServiceImage.updateImage(listImagesLocal,enviroment)

                # Validate Rif Juridica
                result_riff = JuridicaSerializer.validate_riff_peju(request.data['riff_peju'],instance.id)
                if result_riff == True:
                    return message.ShowMessage("RIF no permitido, porque se encuentra asignado a otra Empresa")

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.riff_peju      = str(self.request.data.get("riff_peju")).strip().upper()
                instance.raso_peju      = str('' if self.request.data.get("raso_peju") is None else self.request.data.get("raso_peju")).strip().upper()
                instance.dofi_peju      = str('' if self.request.data.get("dofi_peju") is None else self.request.data.get("dofi_peju")).strip().upper()
                instance.ivaa_peju      = str('' if self.request.data.get("ivaa_peju") is None else self.request.data.get("ivaa_peju")).strip().upper()
                instance.islr_peju      = str('' if self.request.data.get("islr_peju") is None else self.request.data.get("islr_peju")).strip().upper()
                instance.desc_peju      = str('' if self.request.data.get("desc_peju") is None else self.request.data.get("desc_peju")).strip().upper()
                instance.fori_peju      = None if json_foto_riff is None else json_foto_riff
                instance.folo_peju      = None if json_foto_loca is None else json_foto_loca
                instance.fevi_peju      = None if self.request.data.get("fevi_peju") is None else self.request.data.get("fevi_peju")
                instance.pure_peju      = str('' if self.request.data.get("pure_peju") is None else self.request.data.get("pure_peju")).strip().upper()
                instance.codi_ciud_id   = Ciudad.objects.get(id = self.request.data.get("codi_ciud"))
                instance.codi_sect_id   = Sector.objects.get(id = self.request.data.get("codi_sect"))
                instance.codi_tiem_id   = TipoEmpresa.objects.get(id = self.request.data.get("codi_tiem"))
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()

                #   Check Save Contacts
                if isinstance(self.request.data.get("contacts"),list):
                    Contacto.delete_contact("codi_juri",instance.id)
                    for contact in self.request.data.get("contacts"):
                        result_contact = Contacto.check_contact(contact['codi_cont'],contact['codi_grou'])
                        if result_contact == False:
                            contact = Contacto(
                                desc_cont      = contact['codi_cont']
                                ,codi_grco_id   = contact['codi_grou']
                                ,codi_juri_id   = instance.id
                                ,created        = datetime.now()
                                ,updated        = datetime.now()
                            )
                            contact.save()
                return message.UpdateMessage(" La informacion de la Persona Juridica con el Identificador: "+str(instance.id))
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class JuridicaDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    # queryset = Juridica.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_juridic = Juridica.get_queryset().get(id=kwargs['id'])
            result_juridic.deleted = datetime.now()
            result_juridic.save()
            # Deleted in Seller, Supplier, Customer
            return message.DeleteMessage('Persona Juridica '+str(result_juridic.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Persona Juridica no Registrado")

""" Drop Down Juridica """
class JuridicaComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = JuridicaBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Juridica.objects.all().order_by('-id')
        show = self.request.query_params.get('show',None)        
        customer = self.request.query_params.get('customer',None)
        _selectCustomer = self.request.query_params.get('id',None)

        # Parameter Customer
        if customer == 'true':
            queryCustomer = Juridica.objects.filter(id = _selectCustomer) if _selectCustomer == 1 else Juridica.objects.filter(id__in=[_selectCustomer,1])
            query= Juridica.objects.filter(
                ~Exists(Cliente.objects.filter(codi_juri =OuterRef('pk')))
                )
            queryCustomer = queryCustomer.union(query).order_by('-id')
            return queryCustomer

        if show =='true':
            return queryset.all()
        if show =='false' or show is None:
            return queryset.filter(deleted__isnull=True)