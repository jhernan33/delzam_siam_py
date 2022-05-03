from django.shortcuts import render
from rest_framework import generics, status

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Estado
from asiam.serializers import EstadoSerializer
from asiam.paginations import SmallResultsSetPagination

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http import HttpResponse

class EstadoListView(generics.ListAPIView):
    serializer_class = EstadoSerializer
    permission_classes = ()
    queryset = Estado.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = (df.SearchFilter, )
    search_fields = ('id', )
    ordering_fields = ('id', )


class EstadoCreateView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = EstadoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #return self.create(request, *args, **kwargs)

    # serializer_class = EstadoSerializer
    # queryset = Estado.objects.all()
    #permission_classes = (IsAuthenticated, )
    # def post(self, request):
    #     print(request.POST)

    # return HttpResponse(request.POST.items())
    # tutorial_data = JSONParser().parse(request)
    # estados_serializer = EstadoSerializer(data=tutorial_data)
    # if estados_serializer.is_valid():
    #     estados_serializer.save()
    #     return JsonResponse(estados_serializer.data, status=status.HTTP_201_CREATED) 
    # return JsonResponse(estados_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EstadoRetrieveView(generics.RetrieveAPIView):
    serializer_class = EstadoSerializer
    permission_classes = ()
    queryset = Estado.objects.all()
    lookup_field = 'id'

class EstadoUpdateView(generics.UpdateAPIView):
    serializer_class = EstadoSerializer
    permission_classes = ()
    queryset = Estado.objects.all()
    lookup_field = 'id'    

class EstadoDestroyView(generics.DestroyAPIView):
    permission_classes = []

    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    serializer_class = EstadoSerializer    
    queryset = Estado.objects.all()
    lookup_field = 'id'

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

    
    

    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
        #queryset = Estados.objects.filter()
    #permission_classes = ()
    #queryset = Estados.objects.all()
    #return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    #lookup_field = 'id'
    # def get(self,request,pk):
    #     todo = Estado.objects.get(id=pk)
    #     todo_instance = todo.objects.get(id=pk)
    #     todo_instance.delete()
    #     return Response('')

class EstadoComboView(generics.ListAPIView):
    permission_classes = []
    serializer_class = EstadoSerializer    
    lookup_field = 'id'
    queryset = Estado.objects.all()
    
    def list(self, request, *args, **kwargs):
        pais_id = self.kwargs['id']
        paises = get_object_or_404(Estado,id=pais_id)
        estados = Estado.objects.filter(codi_pais_id=pais_id)
        ser = EstadoSerializer(estados,many=True).data
        return Response(ser, status=status.HTTP_200_OK)
    
