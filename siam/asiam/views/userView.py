from datetime import datetime
from unittest import result
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from asiam.serializers import SignupSerializer, UserLoginSerializer

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
    # serializer_class = UserSerializer
    """This api will handle signup"""
    def post(self,request):
            serializer = SignupSerializer(data = request.data)
            if serializer.is_valid():
                    """If the validation success, it will created a new user."""
                    serializer.save()
                    res = { 'status' : status.HTTP_201_CREATED }
                    return Response(res, status = status.HTTP_201_CREATED)
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