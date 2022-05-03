from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Sector
from asiam.serializers import SectorSerializer
from asiam.paginations import SmallResultsSetPagination

class SectorListView(generics.ListAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class SectorCreateView(generics.CreateAPIView):
    serializer_class = SectorSerializer
    #permission_classes = (IsAuthenticated, )
    permission_classes = ()

class SectorRetrieveView(generics.RetrieveAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.objects.all()
    lookup_field = 'id'

class SectorUpdateView(generics.UpdateAPIView):
    serializer_class = SectorSerializer
    permission_classes = ()
    queryset = Sector.objects.all()
    lookup_field = 'id'    

class SectorDestroyView(generics.DestroyAPIView):
    permission_classes = ()
    queryset = Sector.objects.all()
    lookup_field = 'id'
