from .base import Base
from django.db import models

class Ruta(Base):
    codi_zona = models.ForeignKey(
        'Zona',
        on_delete=models.CASCADE,
        related_name='Zona',
    )
    nomb_ruta = models.CharField    ('Nombre de la Ruta', max_length=200, null=True, blank=True)
    posi_ruta = models.IntegerField('Posicion de la Ruta',null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"ruta"'
    
    def save(self, **kwargs):
        self.nomb_ruta = self.nomb_ruta.upper()
        return super().save(**kwargs)

    def get_queryset():
        return Ruta.objects.all().filter(deleted__isnull=True)


    """
    Buscar las rutas por Zona
    """
    def getRouteFilterZone(_zoneId):
        return Ruta.objects.all().filter(codi_zona = _zoneId).values("id")