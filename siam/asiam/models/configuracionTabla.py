from .base import Base
from django.db import models

class ConfiguracionTabla(Base):
    nomb_tabl = models.CharField    ('Nombre de la Tabla',    max_length=100, null=True, blank=True, default='')
    nomb_esqu = models.CharField  ('Nombre del Esquema',    max_length=100, null=True, blank=True, default='')

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"configuracion_tabla"'

    def get_queryset():
        return ConfiguracionTabla.objects.all().filter(deleted__isnull=True)