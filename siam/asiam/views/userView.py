from datetime import datetime
from unittest import result
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from asiam.serializers import SignupSerializer, UserLoginSerializer
from asiam.views.baseMensajeView import BaseMessage
from asiam.models import Profile

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email
        })

class SignupView(generics.CreateAPIView):
    permission_classes = ()
    
    """This api will handle signup"""
    def post(self,request):
        message = BaseMessage
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
                """If the validation success, it will created a new user."""
                # serializer.save()
                try:
                    with transaction.atomic():
                        user = User(username = self.request.data.get("username"))
                        user.password = SignupSerializer.encrypt_password(self.request.data.get('password'))
                        user.is_superuser = True if self.request.data.get("is_superuser")=="true" else False
                        user.first_name = self.request.data.get('first_name')
                        user.last_name = self.request.data.get('last_name')
                        user.email = self.request.data.get('email')
                        user.save()
                        # Save Group
                        user.groups.add(self.request.data.get('group'))
                        # Save Profile
                        profile = Profile(
                            user = User.objects.get(id = user.id)
                        )
                        profile.save()
                        return message.SaveMessage("Creado Exitosamente el Usuario")
                except ObjectDoesNotExist:
                    return message.NotFoundMessage("Error al Guardar el usuario")
        res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data' : serializer.errors }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                ''' We are reterving the token for authenticated user '''
                token ,created = Token.objects.get_or_create(user = user)
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "Token": token.key
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or Password",
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": serializer.errors
                }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

# Close Session
class LogoutView(generics.CreateAPIView):
    permission_classes = ()
    def post(self, request):
        # Borramos de la request la informacion de sesion
        logout(request)

        # Devolvemos la respuesta al cliente
        return Response(status=status.HTTP_200_OK)