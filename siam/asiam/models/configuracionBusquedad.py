from .base import Base
from django.db import models

class ConfiguracionBusquedad(Base):
    nomb_camp = models.CharField    ('Nombre del Campo',    max_length=100, null=True, blank=True, default='')
    titu_camp = models.CharField    ('Titulo del Campo',    max_length=100, null=True, blank=True, default='')
    busc_camp = models.BooleanField ('Permite realizar busquedad por el Campo',null=True, blank=True, default=False)
    orde_camp = models.BooleanField ('Permite ordenar por el Campo',null=True, blank=True, default=False)
    codi_tabl = models.ForeignKey(
        'ConfiguracionTabla',
        on_delete=models.CASCADE,
        related_name='configuraciontabla.codi_tabl+'
    )

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"configuracion_busquedad"'

    def get_queryset():
        return ConfiguracionBusquedad.objects.all().filter(deleted__isnull=True)