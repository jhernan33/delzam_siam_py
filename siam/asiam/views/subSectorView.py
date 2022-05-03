from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import SubSector
from asiam.serializers import SubSectorSerializer
from asiam.paginations import SmallResultsSetPagination

class SubSectorListView(generics.ListAPIView):
    serializer_class = SubSectorSerializer
    permission_classes = ()
    queryset = SubSector.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class SubSectorCreateView(generics.CreateAPIView):
    serializer_class = SubSectorSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class SubSectorRetrieveView(generics.RetrieveAPIView):
    serializer_class = SubSectorSerializer
    permission_classes = ()
    queryset = SubSector.objects.all()
    lookup_field = 'id'

class SubSectorUpdateView(generics.UpdateAPIView):
    serializer_class = SubSectorSerializer
    permission_classes = ()
    queryset = SubSector.objects.all()
    lookup_field = 'id'    

class SubSectorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = SubSector.objects.all()
    lookup_field = 'id'
