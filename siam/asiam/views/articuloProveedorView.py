from datetime import datetime
from os import environ
import os
from django.http import JsonResponse
from django.shortcuts import render
from requests import delete
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import ArticuloProveedor, Articulo, Proveedor
from asiam.serializers import ArticuloProveedorSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView
from django.conf import settings
from django.conf.urls.static import static


class ArticuloProveedorListView(generics.ListAPIView):
    serializer_class = ArticuloProveedorSerializer
    permission_classes = ()
    queryset = ArticuloProveedor.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','codi_arti','codi_prov']
    search_fields = ['id','codi_arti','codi_prov']
    ordering_fields = ['id','codi_arti','codi_prov']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = ArticuloProveedor.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)

class ArticuloProveedorCreateView(generics.CreateAPIView):
    serializer_class = ArticuloProveedorSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):        
        message = BaseMessage
        try:
            result_articulo = Articulo.get_queryset().filter(id = self.request.data.get("codi_arti"))
            result_proveedor = Proveedor.get_queryset().filter(id = self.request.data.get("codi_prov"))

            if result_articulo.count() > 0 and result_proveedor.count() >0:
                try:
                    articuloProveedor = ArticuloProveedor(
                         codi_arti_id      = self.request.data.get("codi_arti")
                        ,codi_prov_id      = self.request.data.get("codi_prov")
                        ,codi_arti_prov    = self.request.data.get("codi_arti_prov")
                        ,obse_arti_prov    = self.request.data.get("obse_arti_prov")
                        ,created           = datetime.now()
                    )
                    articuloProveedor.save()
                    return message.SaveMessage('Articulo Proveedor guardado Exitosamente')
                except Exception as e:
                    return message.ErrorMessage("Error al Intentar Guardar el Articulo Proveedor: "+str(e))
            elif result_articulo.count()<=0:
                return message.ShowMessage('Registro Articulo no Registrado')
            elif result_proveedor.count()<=0:
                return message.ShowMessage('Regustro de Proveedor no Registrado')
        except Articulo.DoesNotExist:
            return message.NotFoundMessage("Id del Articulo Proveedor no Registrado")


class ArticuloProveedorRetrieveView(generics.RetrieveAPIView):
    serializer_class = ArticuloProveedorSerializer
    permission_classes = ()
    queryset = ArticuloProveedor.get_queryset()
    lookup_field = 'id'
    
    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = ArticuloProveedor.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id del Articulo Proveedor no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)


class ArticuloProveedorUpdateView(generics.UpdateAPIView):
    serializer_class = ArticuloProveedorSerializer
    permission_classes = ()
    queryset = ArticuloProveedor.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id del Articulo Proveedor no Registrado")
        else:
            try:
                # Validate Id Articulo
                result_articulo = ArticuloProveedorSerializer.validate_codi_arti(request.data['codi_arti'])
                if result_articulo == False:
                    return message.ErrorMessage("Codi_Arti no es un Valor Valido de Articulo")

                # Validate Id Proveedor
                result_proveedor = ArticuloProveedorSerializer.validate_codi_prov(request.data['codi_prov'])
                if result_proveedor == False:
                    return message.ErrorMessage("Codi_Prov no es un Valor Valido de Proveedor")

                Deleted = request.data['erased']
                if Deleted:
                    isdeleted = datetime.now()
                else:
                    isdeleted = None

                instance.codi_arti_id = request.data['codi_arti']
                instance.codi_prov_id = request.data['codi_prov']
                instance.codi_arti_prov = request.data['codi_arti_prov']
                instance.deleted = isdeleted
                instance.obse_arti_prov = request.data['obse_arti_prov']
                instance.updated = datetime.now()
                instance.save()
                return message.UpdateMessage({"id":instance.id,"codi_arti":instance.codi_arti_id,"codi_prov":instance.codi_prov_id})
            except Exception as e:
                return message.ErrorMessage("Error al Intentar Actualizar:"+str(e))

class ArticuloProveedorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = ArticuloProveedor.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_articulo_proveedor = ArticuloProveedor.get_queryset().get(id=kwargs['id'])
            result_articulo_proveedor.deleted = datetime.now()
            result_articulo_proveedor.save()
            return message.DeleteMessage('Articulo Proveedor '+str(result_articulo_proveedor.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id del Articulo Proveedor no Registrado")

class ArticuloProveedorComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ArticuloProveedorSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = ArticuloProveedor.get_queryset().order_by('-id')
        return queryset