from datetime import datetime
import re
from unittest import result
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from asiam.models import Contacto,GrupoCategoriaContacto,Cliente,Proveedor,Vendedor,Natural,Juridica,Accionista
from asiam.serializers import ContactoSerializer, ContactoBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage

class ContactoListView(generics.ListAPIView):
    serializer_class = ContactoSerializer
    permission_classes = ()
    queryset = Contacto.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ('id','desc_cont')
    ordering_fields = ('id', 'desc_cont')
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Contacto.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)

class ContactoCreateView(generics.CreateAPIView):
    serializer_class = ContactoSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            desc_cont = str(self.request.data.get("desc_cont")).upper().strip()
            # Check Values
            codi_clie = None if self.request.data.get("codi_clie") is None else Cliente.get_queryset().get(id = self.request.data.get("codi_clie"))
            codi_prov = None if self.request.data.get("codi_prov") is None else Proveedor.get_queryset().get(id = self.request.data.get("codi_prov"))
            codi_vend = None if self.request.data.get("codi_vend") is None else Vendedor.get_queryset().get(id = self.request.data.get("codi_vend"))
            codi_natu = None if self.request.data.get("codi_natu") is None else Natural.get_queryset().get(id = self.request.data.get("codi_natu"))
            codi_juri = None if self.request.data.get("codi_juri") is None else Juridica.get_queryset().get(id = self.request.data.get("codi_juri"))
            codi_acci = None if self.request.data.get("codi_acci") is None else Accionista.get_queryset().get(id = self.request.data.get("codi_acci"))

            result_Contacto = Contacto.get_queryset().filter(desc_cont = desc_cont)
            if result_Contacto.count() <= 0:
                try:
                    contacto = Contacto(
                        desc_cont = desc_cont,
                        codi_clie = codi_clie,
                        codi_prov = codi_prov,
                        codi_vend = codi_vend,
                        codi_natu = codi_natu,
                        codi_juri = codi_juri,
                        codi_acci = codi_acci,
                        codi_grco = GrupoCategoriaContacto.get_queryset().get(id = self.request.data.get("codi_grco")),
                        created  = datetime.now()
                    )
                    contacto.save()
                    return message.SaveMessage({"id":Contacto.id,"desc_cont":Contacto.desc_cont})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar el Contacto: "+str(e))
            elif result_Contacto.count()>0:
                return message.ShowMessage({'information':desc_cont,'message':"Ya Registrada"})
        except Contacto.DoesNotExist:
            return message.NotFoundMessage("Id de Contacto no Registrado")
         
class ContactoRetrieveView(generics.RetrieveAPIView):
    serializer_class = ContactoSerializer
    permission_classes = ()
    queryset = Contacto.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Contacto.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Contacto no Registrado")  
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class ContactoUpdateView(generics.UpdateAPIView):
    serializer_class = ContactoSerializer
    permission_classes = ()
    queryset = Contacto.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Contacto no Registrado")
        else:
            try:
                # Check Values
                codi_grco = GrupoCategoriaContacto.get_queryset().get(id = self.request.data.get("codi_grco"))
                codi_clie = None if self.request.data.get("codi_clie") is None else Cliente.get_queryset().get(id = self.request.data.get("codi_clie"))
                codi_prov = None if self.request.data.get("codi_prov") is None else Proveedor.get_queryset().get(id = self.request.data.get("codi_prov"))
                codi_vend = None if self.request.data.get("codi_vend") is None else Vendedor.get_queryset().get(id = self.request.data.get("codi_vend"))
                codi_natu = None if self.request.data.get("codi_natu") is None else Natural.get_queryset().get(id = self.request.data.get("codi_natu"))
                codi_juri = None if self.request.data.get("codi_juri") is None else Juridica.get_queryset().get(id = self.request.data.get("codi_juri"))
                codi_acci = None if self.request.data.get("codi_acci") is None else Accionista.get_queryset().get(id = self.request.data.get("codi_acci"))

                # Validate Description Contacto
                result_Contacto = Contacto.objects.filter(desc_cont = self.request.data.get("desc_cont").upper().strip()).filter(codi_grco = codi_grco)
                if result_Contacto.count() > 0:
                    if result_Contacto[0].id != instance.id:
                        return message.ShowMessage("Descripcion de Contacto ya Registrada con el ID:"+str(result_Contacto[0].id))

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                if codi_clie:
                    instance.codi_clie = codi_clie
                if codi_prov:
                    instance.codi_prov = codi_prov
                if codi_vend:
                    instance.codi_vend = codi_vend
                if codi_natu:
                    instance.codi_natu = codi_natu
                if codi_juri:
                    instance.codi_juri = codi_juri
                if codi_acci:
                    instance.codi_acci = codi_acci
                instance.desc_cont = request.data['desc_cont'].upper().strip()
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()
                
                return message.UpdateMessage({"id":instance.id,"desc_cont":instance.desc_cont})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class ContactoDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Contacto.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_Contacto = Contacto.get_queryset().get(id=kwargs['id'])
            result_Contacto.deleted = datetime.now()
            result_Contacto.save()
            return message.DeleteMessage('Contacto '+str(result_Contacto.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Contacto no Registrado")

# Drop Down
class ContactoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ContactoBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Contacto.objects.all()
        show = self.request.query_params.get('show',None)
            
        if show =='true':
            return queryset.all()
        if show =='false' or show is None:
            return queryset.filter(deleted__isnull=True)
        