
from .base import Base
from django.db import models

class Ciudad(Base):
    nomb_ciud = models.CharField    ('nomb_ciud',  max_length=200, null=False, blank=False, default='')
    codi_esta = models.ForeignKey(
        'Estado',
        on_delete=models.CASCADE,
        related_name='Estado',
    )

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"ciudad"'

    def save(self, **kwargs):
        self.nomb_ciud = self.nomb_ciud.upper()
        return super().save(**kwargs)

    def get_queryset():
        return Ciudad.objects.all().filter(deleted__isnull=True)