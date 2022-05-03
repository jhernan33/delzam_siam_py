from .base import Base
from django.db import models

class Zona(Base):
    desc_zona = models.CharField    ('Nombre de la Zona', max_length=200, null=False, blank=False, default='', unique=True)

    class Meta:
        ordering = ['desc_zona']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"zona"'
