from datetime import datetime
from unittest import result
from rest_framework import status, generics
from asiam.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token

class SignupView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = ()
    # serializer_class = VendedorSerializer
    def post(self, request):
        # Recuperamos las credenciales y autenticamos al usuario
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username= username, password=password)

        # Si es correcto añadimos a la request la informacion de sesion
        if user:
            login(request,user)
            token, created = Token.objects.get_or_create(user=user)
            token.created = datetime.utcnow()
            token.save()
            
            return Response({"user":UserSerializer(user).data,
            "access_token":token.key,
            "expires_in":token.created},status=status.HTTP_201_CREATED)
            # return Response(UserSerializer(user).data,status=status.HTTP_200_OK)
        
        # si no es correcto devolvemos un error en la peticion
        return Response({'result':'Datos Incorrectos, verifique e intenten de nuevo'},status=status.HTTP_404_NOT_FOUND)

# Close Session
class LogoutView(generics.CreateAPIView):
    permission_classes = ()
    def post(self, request):
        print(request)
        # Borramos de la request la informacion de sesion
        logout(request)
        print(request)

        # Devolvemos la respuesta al cliente
        return Response(status=status.HTTP_200_OK)