from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models, connection
from .base import Base

class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=120, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=75, blank=True)
    profile_picture = models.JSONField ('Foto del Perfil',null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"public\".\"profile"'

    def get_queryset():
        return Profile.objects.all().filter(deleted__isnull=True)
    
    """ Get Instance Profile """
    def getInstanceProfile(Id):
        return Profile.objects.get(id = Id)