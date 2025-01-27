from os import environ
import os
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.exceptions import ObjectDoesNotExist

from asiam.models import Pedido
from asiam.serializers import HistoricalOrderSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class HistoricalOrderSearchView(generics.ListAPIView):
    serializer_class = HistoricalOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pedido.get_queryset()
    # pagination_class = SmallResultsSetPagination
    ordering = ['-id']

    def get_queryset(self):
        # Filter Except orders history
        queryset = Pedido.objects.all()
        _historical = 7,8
        
        queryset = queryset.filter(codi_espe__in = _historical )
        
        invoice_number = str(self.request.query_params.get('invoice')).upper().strip()
        if invoice_number:
            queryset = queryset.filter(nufa_pedi__icontains = invoice_number)
        
        show = self.request.query_params.get('show')
        if show =='true':
            return queryset.filter(deleted__isnull=False)
        if show =='all':
            return queryset

        return queryset.filter(deleted__isnull=True)