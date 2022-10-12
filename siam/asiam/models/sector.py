from email.policy import default
from .base import Base
from django.db import models

class Sector(Base):
    codi_ciud = models.ForeignKey(
        'Ciudad',
        on_delete=models.CASCADE,
        related_name='Ciudad',
    )
    nomb_sect = models.CharField ('Nombre del Sector', max_length=200, null=False, blank=False,default='')

    class Meta:
        unique_together =('nomb_sect','codi_ciud')
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"sector"'

    def save(self, *args, **kwargs):
        self.nomb_sect = self.nomb_sect.upper()
        return super(Sector,self).save(*args, **kwargs)    

    def get_queryset():
        return Sector.objects.all().filter(deleted__isnull=True)