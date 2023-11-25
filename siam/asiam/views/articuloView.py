from datetime import datetime
from os import environ
import os
from django.http import JsonResponse
from django.shortcuts import render
from requests import delete
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import FormParser,MultiPartParser
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Articulo
from asiam.serializers import ArticuloSerializer, ArticuloComboSerializer
from asiam.paginations import SmallResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from asiam.views.baseMensajeView import BaseMessage
from .serviceImageView import ServiceImageView
from django.conf import settings
from django.conf.urls.static import static
import dbf
from datetime import datetime, timezone


class ArticuloListView(generics.ListAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    queryset = Articulo.get_queryset()
    pagination_class = SmallResultsSetPagination
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['id','desc_arti','idae_arti','codi_arti','codi_sufa__desc_sufa','codi_sufa__abae_sufa','codi_sufa__codi_fami__desc_fami','codi_sufa__codi_fami__abae_fami']
    search_fields = ['id','desc_arti','idae_arti','codi_arti','codi_sufa__desc_sufa','codi_sufa__abae_sufa','codi_sufa__codi_fami__desc_fami','codi_sufa__codi_fami__abae_fami']
    ordering_fields = ['id','desc_arti','idae_arti','codi_arti','codi_sufa__desc_sufa','codi_sufa__abae_sufa','codi_sufa__codi_fami__desc_fami','codi_sufa__codi_fami__abae_fami']
    ordering = ['-id']

    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Articulo.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset
        return queryset.filter(deleted__isnull=True)

class ArticuloCreateView(generics.CreateAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    
    def create(self, request, *args, **kwargs):
        listImages = request.data['foto_arti']
        enviroment = os.path.realpath(settings.WEBSERVER_ARTICLE)
        ServiceImage = ServiceImageView()
        json_images = ServiceImage.saveImag(listImages,enviroment)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['foto_arti'] = json_images
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        message = BaseMessage
        return message.SaveMessage(serializer.data)

class ArticuloRetrieveView(generics.RetrieveAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    queryset = Articulo.get_queryset()
    lookup_field = 'id'
    
    def get_queryset(self):
        show = self.request.query_params.get('show')
        queryset = Articulo.objects.all()
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        
        return queryset.filter(deleted__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Articulo no Registrado")
        else:
            serialize = self.get_serializer(instance)
            return message.ShowMessage(self.serializer_class(instance).data)

class ArticuloUpdateView(generics.UpdateAPIView):
    serializer_class = ArticuloSerializer
    permission_classes =  []
    queryset = Articulo.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            instance = self.get_object()
        except Exception as e:
            return message.NotFoundMessage("Id de Articulo no Registrado")
        else:
            listImages = request.data['foto_arti']
            enviroment = os.path.realpath(settings.WEBSERVER_ARTICLE)
            ServiceImage = ServiceImageView()
            json_images = ServiceImage.updateImage(listImages,enviroment)
            Deleted = request.data['erased']
            if Deleted:
                isdeleted = datetime.now()
            else:
                isdeleted = None
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated = datetime.now(), foto_arti = json_images, deleted = isdeleted)
                return message.UpdateMessage(serializer.data)
            else:
                return message.ErrorMessage("Error al Intentar Actualizar Articulo")

class ArticuloDestroyView(generics.DestroyAPIView):
    permission_classes =  []
    queryset = Articulo.get_queryset()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        message = BaseMessage
        try:
            result_city = Articulo.get_queryset().get(id=kwargs['id'])
            result_city.deleted = datetime.now()
            result_city.save()
            return message.DeleteMessage('Articulo '+str(result_city.id))
        except ObjectDoesNotExist:
            return message.NotFoundMessage("Id de Articulo no Registrado")

class ArticuloComboView(generics.ListAPIView):
    permission_classes =  []
    serializer_class = ArticuloComboSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Articulo.get_queryset().order_by('desc_arti')
        return queryset
    
    def get_queryset(self):
        if self.request.query_params.get('subfamily') == None:
            queryset = Articulo.get_queryset().order_by('desc_arti')
        else:
            queryset = Articulo.get_queryset().filter(codi_sufa=self.request.query_params.get('subfamily')).order_by('desc_arti')
        return queryset

'''
    Import data from system clipper
'''
def ImportDataArticle(_source):
    import math

    table = dbf.Table(_source)
    table.open(dbf.READ_WRITE)
    for record in table:
        # print([record.A05REF, record.COD_ANT, record.A05DES])
        article_code = str(record.A05REF).strip().upper()
        article_quantity_min = record.A05MIN
        article_quantity_max = record.A05MAX
        article_porcentague_one = record.A05POR1
        article_porcentague_two = record.A05POR2
        article_porcentague_three = record.A05POR3
        article_porcentague_four = record.A05POR4
        article_existence = record.A05EXI
        article_cost = record.A05NUE
        article_description = str(record.A05DES).strip().upper()
        article_reference = str(record.A05REF1).strip().upper()
        if article_cost is not None:
            # article_cost = float("{:.2f}",format(record.A05COS))
            # article_cost = round(float(record.A05COS),2)
            my_formatter = "{0000:.2f}"
            article_cost = my_formatter.format(record.A05NUE)
            #article_cost = float(format(record.A05COS, '.2f'))
            result = Articulo.objects.filter(codi_arti = article_reference).update(
                updated = datetime.now()
                , ppre_arti = article_cost
                , cmin_arti = article_quantity_min
                , cmax_arti = article_quantity_max
                , por1_arti = article_porcentague_one
                , por2_arti = article_porcentague_two
                , por3_arti = article_porcentague_three
                , por4_arti = article_porcentague_four
                , exis_arti = article_existence
                , desc_arti = article_description
                # Code Old
                , idae_arti = article_code
                )
    table.close()

'''
    Import Data From CSV SIAE
'''
def ImportDataArticleSiae(_source):
    import os
    import pandas as pd
    enviroment = os.path.realpath(settings.UPLOAD_FILES)

    df = pd.read_csv(enviroment+_source)

    # print(df.to_string())
    frame = pd.DataFrame(df,columns=['codi_arti','desc_arti','por1_arti','por2_arti','por3_arti','ppre_arti','exgr_arti','dire_foto','idae_arti','esta__tus'])

    for k in frame.index:
        article_code = str(frame['idae_arti'][k]).strip().upper()
        # article_quantity_min = record.A05MIN
        # article_quantity_max = record.A05MAX
        article_porcentague_one = frame['por1_arti'][k]
        article_porcentague_two = frame['por2_arti'][k]
        article_porcentague_three = frame['por3_arti'][k]
        # article_porcentague_four = record.A05POR4
        # article_existence = frame['codi_arti'][k]
        article_cost = frame['ppre_arti'][k]
        article_description = str(frame['desc_arti'][k]).strip().upper()
        article_reference = str(frame['codi_arti'][k]).strip().upper()
        if article_cost is not None:
            # article_cost = float("{:.2f}",format(record.A05COS))
            # article_cost = round(float(record.A05COS),2)
            my_formatter = "{0000:.2f}"
            article_cost = my_formatter.format(article_cost)
            result_article = Articulo.objects.filter(codi_arti = article_reference)
            if result_article.count() <= 0:
                # Save Article
                object_article = Articulo(
                    created  = datetime.now()
                    , ppre_arti = article_cost
                    , por1_arti = article_porcentague_one
                    , por2_arti = article_porcentague_two
                    , por3_arti = article_porcentague_three
                    , desc_arti = article_description
                    # Code Old
                    , idae_arti = article_code
                    )
                object_article.save()
            else:
                result_article.update(
                    updated = datetime.now()
                    ,ppre_arti = article_cost
                    #, cmin_arti = article_quantity_min
                    #, cmax_arti = article_quantity_max
                    ,por1_arti = article_porcentague_one
                    ,por2_arti = article_porcentague_two
                    ,por3_arti = article_porcentague_three
                    #, por4_arti = article_porcentague_four
                    # , exis_arti = article_existence
                    ,desc_arti = article_description
                    # Code Old
                    ,idae_arti = article_code
                )
    