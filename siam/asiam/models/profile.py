from django.contrib.auth.models import User
from django.db import models, connection
from .base import Base

class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=120, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture', blank=True)
    phone_number = models.CharField(max_length=75, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"public\".\"profile"'

    def get_queryset():
        return Profile.objects.all().filter(deleted__isnull=True)

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return None
    
    """ Get Instance Profile """
    def getInstanceProfile(Id):
        return Profile.objects.get(id = Id)