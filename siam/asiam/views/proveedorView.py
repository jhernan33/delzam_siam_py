from datetime import datetime
from difflib import restore
from os import environ
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Proveedor, Juridica, Natural
from asiam.serializers import ProveedorSerializer, NaturalSerializer, ProveedorBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView
from django.conf import settings
from django.conf.urls.static import static


class ProveedorListView(generics.ListAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    try:
        message = BaseMessage    
        queryset = Proveedor.get_queryset()
        pagination_class = SmallResultsSetPagination
        filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
        search_fields   = ['id','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','codi_juri__dofi_peju','codi_repr__prno_pena','codi_repr__seno_pena','codi_repr__prap_pena','codi_repr__seap_pena']
        ordering_fields = ['id','codi_natu__prno_pena','codi_natu__seno_pena','codi_natu__prap_pena','codi_natu__seap_pena','codi_juri__riff_peju','codi_juri__raso_peju','codi_juri__dofi_peju','codi_repr__prno_pena','codi_repr__seno_pena','codi_repr__prap_pena','codi_repr__seap_pena']
        ordering = ['-id']

        def get_queryset(self):
            show = self.request.query_params.get('show')
            queryset = Proveedor.objects.all()
            if show =='true':
                return queryset.filter(deleted__isnull=False)
            if show =='all':
                return queryset
            return queryset.filter(deleted__isnull=True)
    except Exception as e:
        message.ErrorMessage("Error al Listar el Proveedor: "+str(e))

class ProveedorCreateView(generics.CreateAPIView):
    serializer_class = ProveedorBasicSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_juridica = Juridica.get_queryset().filter(id = self.request.data.get("codi_juri"))
            result_natural = Natural.get_queryset().filter(id = self.request.data.get("codi_natu"))
            result_representante = Natural.get_queryset().filter(id = self.request.data.get("codi_repr"))

            if result_juridica.count() > 0 and result_natural.count() >0 and result_representante.count()>0:
                enviroment = os.path.realpath(settings.WEBSERVER_SUPPLIER)
                ServiceImage = ServiceImageView()
                try:
                    json_foto_prov = None
                    if request.data['foto_prov'] is not None:
                        listImagesProv  = request.data['foto_prov']
                        json_foto_prov  = ServiceImage.saveImag(listImagesProv,enviroment)
                    proveedor = Proveedor(
                        codi_natu_id       = self.request.data.get("codi_natu")
                        ,codi_juri_id      = self.request.data.get("codi_juri")
                        ,codi_repr_id      = self.request.data.get("codi_repr")
                        ,mocr_prov         = self.request.data.get("mocr_prov")
                        ,plcr_prov         = self.request.data.get("plcr_prov")
                        ,foto_prov         = None if json_foto_prov is None else json_foto_prov
                        ,obse_prov         = self.request.data.get("obse_prov")
                        ,created           = datetime.now()
                    )
                    proveedor.save()
                    return message.SaveMessage({"id":proveedor.id})
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar el Proveedor: "+str(e))
            elif result_juridica.count()<=0:
                return message.ShowMessage('Registro Juridico no Registrado')
            elif result_natural.count()<=0:
                return message.ShowMessage('Persona Natural no Registrada')
        except Proveedor.DoesNotExist:
            return message.NotFoundMessage("Id de Proveedor no Registrado")

class ProveedorRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    queryset = Proveedor.get_queryset()
    lookup_field = 'id'

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Proveedor.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)


    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Proveedor no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class ProveedorUpdateView(generics.UpdateAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    queryset = Proveedor.objects.all()
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Proveedor no Registrado")
        else:
            try:
                # State Deleted
                state_deleted = None
                if instance.deleted:
                    state_deleted = True
                
                Deleted = request.data['erased']
                if Deleted:                    
                    isdeleted = datetime.now()
                else:    
                    isdeleted = None

                # Validate Id Natural
                result_natural = ProveedorSerializer.validate_codi_natu(request.data['codi_natu'],state_deleted)
                if result_natural == False:
                    return message.NotFoundMessage("Codi_Natu no es un Valor Valido de Persona Natural")

                # Validate Id Juridica
                result_juridico = ProveedorSerializer.validate_codi_juri(request.data['codi_juri'],state_deleted)
                if result_juridico == False:
                    return message.NotFoundMessage("Codi_Juri no es un Valor Valido de Persona Juridica")

                # Validate Id Representante
                result_represent = ProveedorSerializer.validate_codi_natu(request.data['codi_repr'],state_deleted)
                if result_represent == False:
                    return message.NotFoundMessage("Codi_Repr no es un Valor Valido de Persona Natural")

                listImages = request.data['foto_prov']
                enviroment = os.path.realpath(settings.WEBSERVER_SUPPLIER)
                ServiceImage = ServiceImageView()
                json_images = ServiceImage.updateImage(listImages,enviroment)
                
                instance.mocr_prov = request.data['mocr_prov']
                instance.plcr_prov = request.data['plcr_prov']
                instance.obse_prov = request.data['obse_prov']
                instance.codi_juri_id = request.data['codi_juri']
                instance.codi_natu_id = request.data['codi_natu']
                instance.codi_repr_id = request.data['codi_repr']
                instance.foto_prov = json_images
                instance.deleted = isdeleted
                instance.updated = datetime.now()
                instance.save()

                # Restore Person: Legal, Natural, Representant
                supplierId =instance.id
                self.restoreSupplier(supplierId)
                return message.UpdateMessage({"id":instance.id,"mocr_prov":instance.mocr_prov,"plcr_prov":instance.plcr_prov})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

    """ Restore Person Legal, Natural, Represent     """
    def restoreSupplier(self,arg):
        queryset = Proveedor.objects.filter(id = arg)
        if queryset.count() >0:
             for supplier in queryset.values():
                naturalId = supplier['codi_natu_id']
                legalId = supplier["codi_juri_id"]
                representantId = supplier["codi_repr_id"]
                # Restore Natural
                Natural.objects.filter(id = naturalId).update(deleted=None)
                # Restore Juridic
                Juridica.objects.filter(id = legalId).update(deleted=None)
                # Restore Represent
                Natural.objects.filter(id = representantId).update(deleted=None)

class ProveedorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Proveedor.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            with transaction.atomic():
                # Delete Supplier
                result_supplier = Proveedor.get_queryset().get(id=kwargs['id'])
                result_supplier.deleted = datetime.now()
                result_supplier.save()
                # Delete Natural
                result_natural = Natural.objects.get(pk=result_supplier.codi_natu_id)
                result_natural.deleted = datetime.now()
                result_natural.save()
                # Delete Legal
                result_legal = Juridica.objects.get(pk=result_supplier.codi_juri_id)
                result_legal.deleted = datetime.now()
                result_legal.save()
                # Delete Represent
                result_represent = Natural.objects.get(pk=result_supplier.codi_repr_id)
                result_represent.deleted = datetime.now()
                result_represent.save()
                return message.DeleteMessage('Proveedor '+str(result_supplier.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Proveedor no Registrado")

class ProveedorComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ProveedorBasicSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Proveedor.get_queryset().order_by('-id').values()
        return queryset

class ProveedorRestore(generics.UpdateAPIView):
    serializer_class = ProveedorSerializer
    permission_classes = ()
    queryset = Proveedor.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Presentacion no Registrada")
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(deleted = None)
                return message.RestoreMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Restaurar Presentacion")