from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as df
from rest_framework.permissions import IsAuthenticated

from asiam.models import Vendedor
from asiam.paginations import SmallResultsSetPagination


    
