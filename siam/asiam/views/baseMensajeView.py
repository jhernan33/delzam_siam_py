from rest_framework.response import Response
from rest_framework import generics, status
from django.http import HttpResponse, JsonResponse

class BaseMessage:

    def SaveMessage(self):
        save = {"message":"Guardado Exitosamente","status":status.HTTP_201_CREATED,"data":self}
        return Response(save,status=status.HTTP_201_CREATED)
    
    def UpdateMessage(self):
        update = {"message":"Actualizado Exitosamente","status":status.HTTP_200_OK,"data":self}
        return Response(update)

    def DeleteMessage(self):
        delete = {"message":"Eliminado con Exito el Registro","status":status.HTTP_200_OK,"data":self}
        return Response(delete)

    def ErrorMessage(self):
        error = {"message":"Error al Realizar la Operacion","status":status.HTTP_500_INTERNAL_SERVER_ERROR,"data":self}
        return Response(error,status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def NotFoundMessage(self):
        message = {"message":"No se Encontro","status":status.HTTP_404_NOT_FOUND,"data":self}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

    def ShowMessage(self):
        message = {"message":"Registro Encontrado","status":status.HTTP_200_OK,"data":self}
        return Response(message,status.HTTP_200_OK)
    
    def RestoreMessage(self):
        update = {"message":"Restaurado Exitosamente","status":status.HTTP_200_OK,"data":self}
        return Response(update)

    def UnauthorizedMessage(self):
        data = {
            'message': "No Autorizado, "+self,
            'state': status.HTTP_401_UNAUTHORIZED
        }
        return JsonResponse(data)