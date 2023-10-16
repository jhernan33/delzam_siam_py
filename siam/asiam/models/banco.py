from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class Banco(Base):
    desc_banc = models.CharField  ('Nombre del Banco', max_length=50, null=True, blank=True, default='', unique=True)
    logo_banc = models.JSONField  ('Foto del Banco',null=True, blank=True)

    class Meta:
        ordering = ['desc_banc']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"banco"'
    
    def get_queryset():
        return Banco.objects.all().filter(deleted__isnull=True)
