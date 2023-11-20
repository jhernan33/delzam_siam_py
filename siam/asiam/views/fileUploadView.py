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
import os
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
            enviroment = os.path.realpath(settings.MEDIA_URL)
            # Place Enviroment
            place = enviroment+'INRA05.DBF'
            ImportDataArticle(place)
            # Remove File
            pathlib.Path(place).unlink(missing_ok=True)

            return message.SaveMessage('Importacion realizado Exitosamente')

        return message.ErrorMessage("Error al Intentar Guardar el Pedido: "+str(serializer.errors))