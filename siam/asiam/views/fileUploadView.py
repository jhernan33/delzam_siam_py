from datetime import datetime
from rest_framework import status
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from asiam.serializers import FileUploadSerializer
from asiam.views import ImportDataArticle
import dbf
import pathlib
import os,uuid
from asiam.views.articuloView import ImportDataArticleSiae
from asiam.views.familiaView import ImportDataFamily
from asiam.views.subFamiliaView import ImportDataSubFamily
from asiam.views.baseMensajeView import BaseMessage
from django.conf import settings

class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        message = BaseMessage
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save(created = datetime.now())
            # Run Migration from dbf to Postgresql MEDIA_URL
            enviroment = os.path.realpath(settings.UPLOAD_FILES)+'/'
            # Place Enviroment
            ext = '.'+'dbf'
            nameFile = str(uuid.uuid4())[:12]
            file_name_new = enviroment + nameFile+str(ext)
            file_name_old = request.FILES['file']
            serializer.save(created = datetime.now(),)
            file_name_old = enviroment + str(file_name_old)

            try:
                os.rename(file_name_old,file_name_new)
            except FileExistsError:
                os.remove(file_name_new)
                # rename it
                os.rename(file_name_old, file_name_new)
            ImportDataArticle(file_name_new)
            # Remove File
            pathlib.Path(file_name_new).unlink(missing_ok=True)

            return message.SaveMessage('Importacion realizado Exitosamente')

        return message.ErrorMessage("Error al Intentar Guardar la Importación: "+str(serializer.errors))

class FileUploadSiaeView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        message = BaseMessage
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save(created = datetime.now())
            # Run Migration from dbf to Postgresql MEDIA_URL
            enviroment = os.path.realpath(settings.UPLOAD_FILES)+'/'
            # Place Enviroment
            ext = '.'+'csv'
            nameFile = str(uuid.uuid4())[:12]
            file_name_new = enviroment + nameFile+str(ext)
            file_name_old = request.FILES['file']
            serializer.save(created = datetime.now(),)
            file_name_old = enviroment + str(file_name_old)

            try:
                os.rename(file_name_old,file_name_new)
            except FileExistsError:
                os.remove(file_name_new)
                # rename it
                os.rename(file_name_old, file_name_new)
            ImportDataArticleSiae(file_name_new)
            # Remove File
            pathlib.Path(file_name_new).unlink(missing_ok=True)

            return message.SaveMessage('Importacion realizado exitosamente')

        return message.ErrorMessage("Error al Intentar Guardar la Importación: "+str(serializer.errors))

'''
    Import Data Family
'''
class FileUploadFamily(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        message = BaseMessage
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            enviroment = os.path.realpath(settings.UPLOAD_FILES)+'/'
            # Place Enviroment
            ext = '.'+'csv'
            nameFile = str(uuid.uuid4())[:12]
            file_name_new = enviroment + nameFile+str(ext)
            file_name_old = request.FILES['file']
            serializer.save(created = datetime.now(),)
            file_name_old = enviroment + str(file_name_old)

            try:
                os.rename(file_name_old,file_name_new)
            except FileExistsError:
                os.remove(file_name_new)
                # rename it
                os.rename(file_name_old, file_name_new)
            # Run Migration from csv to Postgresql MEDIA_URL
            ImportDataFamily(file_name_new)
            # Remove File
            pathlib.Path(file_name_new).unlink(missing_ok=True)

            return message.SaveMessage('Importacion de la información referente a la tabla Familias se ha realizado exitosamente')

        return message.ErrorMessage("Error al Intentar Guardar la Importación: "+str(serializer.errors))
    
'''
    Import Data Subfamily
'''
class FileUploadSubFamily(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        message = BaseMessage
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            enviroment = os.path.realpath(settings.UPLOAD_FILES)+'/'
            # Place Enviroment
            ext = '.'+'csv'
            nameFile = str(uuid.uuid4())[:12]
            file_name_new = enviroment + nameFile+str(ext)
            file_name_old = request.FILES['file']
            serializer.save(created = datetime.now(),)
            file_name_old = enviroment + str(file_name_old)

            try:
                os.rename(file_name_old,file_name_new)
            except FileExistsError:
                os.remove(file_name_new)
                # rename it
                os.rename(file_name_old, file_name_new)
            ImportDataSubFamily(file_name_new)
            # Remove File
            pathlib.Path(file_name_new).unlink(missing_ok=True)

            return message.SaveMessage('Importacion de la informacion de SubFamilias realizado exitosamente')

        return message.ErrorMessage("Error al Intentar Guardar la Importación: "+str(serializer.errors))