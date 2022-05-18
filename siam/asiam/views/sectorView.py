from datetime import datetime
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status


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
    permission_classes = ()
    serializer_class = SectorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(created = datetime.now())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
