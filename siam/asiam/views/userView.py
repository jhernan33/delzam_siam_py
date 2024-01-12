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
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.generic.list import ListView  

from asiam.serializers import SignupSerializer, UserLoginSerializer, UserSerializer, UserResetPasswordSerializer
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
                        user.group = 4 if self.request.data.get('gruop') is None else self.request.data.get('gruop')
                        user.save()
                        # Save Group
                        user.groups.add(self.request.data.get('group'))
                        # Save Profile
                        profile = Profile(
                            user = User.objects.get(id = user.id)
                        )
                        profile.save()
                        # Generate Token
                        token, created = Token.objects.get_or_create(user=user)
                        data = {
                            "token": token.key
                        }
                        return message.SaveMessage(data)
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
                    "token": token.key
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
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            # Devolvemos la respuesta al cliente
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ResetPasswordView(generics.CreateAPIView):
    permission_classes = ()

    """This Endpoint Reset Password"""
    def post(self,request):
        message = BaseMessage
        serializer = UserResetPasswordSerializer(data = request.data)
        username = self.request.data.get("username")
        password = SignupSerializer.encrypt_password(self.request.data.get('password'))
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.password = password
            user.save()

            data = {
                "user": "Reseteada exitosamente la data"
            }
            return message.SaveMessage(data)
        res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data' : serializer.errors }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)