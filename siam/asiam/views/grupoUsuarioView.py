from datetime import datetime
from unittest import result
from rest_framework import status, generics
# from asiam.serializers import GrupoUsuarioSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from asiam.paginations import SmallResultsSetPagination
from rest_framework import filters as df

class GrupoUsuarioListView(generics.ListAPIView):
    # serializer_class = GrupoUsuarioSerializer
    permission_classes = []
    queryset = Group.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class GrupoUsuarioCreateView(generics.CreateAPIView):
    permission_classes = []
    # serializer_class = GrupoUsuarioSerializer    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save(created = datetime.now())

class GrupoUsuarioRetrieveView(generics.RetrieveAPIView):
    # serializer_class = GrupoUsuarioSerializer
    permission_classes = []
    queryset = Group.objects.all()
    lookup_field = 'id'

class GrupoUsuarioUpdateView(generics.UpdateAPIView):
    # serializer_class = GrupoUsuarioSerializer
    permission_classes = ()
    queryset = Group.objects.all()
    lookup_field = 'id'    

class GrupoUsuarioDestroyView(generics.DestroyAPIView):
    permission_classes = []
    # serializer_class = GrupoUsuarioSerializer
    queryset = Group.objects.all()
    lookup_field = 'id'