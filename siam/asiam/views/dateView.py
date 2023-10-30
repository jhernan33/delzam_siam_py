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


from asiam.models import Base
from asiam.serializers import BancoSerializer, BancoComboSerializer, BancoBasicSerializer
from asiam.paginations import SmallResultsSetPagination
from asiam.views.baseMensajeView import BaseMessage

class DateRetrieveView(generics.RetrieveAPIView):
    permission_classes = ()

    def retrieve(self, request, *args, **kwargs):
        message = BaseMessage
        language = self.request.query_params.get('language',None)
        if language is not None and str(language).strip().lower()=='es':
            date = Base.gettingTodaysDate(language)
            return message.ShowMessage(date)

        date = Base.gettingTodaysDate()
        return message.ShowMessage(date)