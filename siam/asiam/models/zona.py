from .base import Base
from django.db import models

class Zona(Base):
    desc_zona = models.CharField    ('Nombre de la Zona', max_length=200, null=False, blank=False, default='', unique=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"zona"'

    def save(self, **kwargs):
        self.desc_zona = self.desc_zona.upper()
        return super().save(**kwargs)

    def get_queryset():
        return Zona.objects.all().filter(deleted__isnull=True)