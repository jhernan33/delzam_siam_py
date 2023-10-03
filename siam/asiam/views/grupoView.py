from datetime import datetime
from unittest import result
from rest_framework import status, generics
from asiam.serializers import GrupoSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from asiam.paginations import SmallResultsSetPagination
from rest_framework import filters as df

class GrupoListView(generics.ListAPIView):
    serializer_class = GrupoSerializer
    permission_classes = []
    queryset = Group.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )

class GrupoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = GrupoSerializer    

    def create(self, request, *args, **kwargs):
        # print(request.data['name'])
        # self.name = str(request.data['name']).upper()
        # print(self.name)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GrupoRetrieveView(generics.RetrieveAPIView):
    serializer_class = GrupoSerializer
    permission_classes = []
    queryset = Group.objects.all()
    lookup_field = 'id'

class GrupoUpdateView(generics.UpdateAPIView):
    serializer_class = GrupoSerializer
    permission_classes = ()
    queryset = Group.objects.all()
    lookup_field = 'id'    

class GrupoDestroyView(generics.DestroyAPIView):
    permission_classes = []
    serializer_class = GrupoSerializer
    queryset = Group.objects.all()
    lookup_field = 'id'