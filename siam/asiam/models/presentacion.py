from .base import Base
from django.db import models

class Presentacion(Base):
    desc_pres = models.CharField ('desc_pres',   max_length=200, null=False, blank=False, default='', unique=True)
    tipo_pres = models.CharField ('tipo_pres',   max_length=1, null=True, blank=True, default='')
    abre_pres = models.CharField ('abre_pres',   max_length=10, null=True, blank=True, default='')

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"presentacion"'

    def save(self, *args, **kwargs):        
        self.desc_pres = self.desc_pres.upper()
        self.tipo_pres = self.tipo_pres.upper()
        self.abre_pres = self.abre_pres.upper()
        return super(Presentacion,self).save(*args, **kwargs)

    def get_queryset():
        return Presentacion.objects.all().filter(deleted__isnull=True)