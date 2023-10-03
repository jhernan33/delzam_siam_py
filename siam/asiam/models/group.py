
from .base import Base
from django.db import models
from django.contrib.auth.models import AbstractUser, GroupManager

class Group(GroupManager):
    
    # def save(self, **kwargs):
    #     self.name = str(self.name).upper()
    #     return super().save(**kwargs)

    def get_queryset():
        return Group.objects.all()