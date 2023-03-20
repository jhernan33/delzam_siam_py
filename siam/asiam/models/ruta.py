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
        if isinstance(_zoneId,str):
            # Create List
            _zoneList = []
            ocu_pri = 0
            # Check Count Ocurrences
            indexes = [i for i, c in enumerate(_zoneId) if c ==',']
            if len(indexes) >0:
                # Iterate Indexes
                for x in indexes:
                    if ocu_pri == 0:
                        _zoneList.append(int(_zoneId[ocu_pri:x]))
                        ocu_pri = x
                    elif ocu_pri > 0:
                        _zoneList.append(int(_zoneId[ocu_pri+1:x]))
                        ocu_pri = x
                _zoneList.append(int(_zoneId[ocu_pri+1:len(_zoneId)]))
            elif len(indexes) ==0:
                _zoneList.append(int(_zoneId[0:len(_zoneId)]))

            _result = Ruta.get_queryset().filter(codi_zona__in = _zoneList).values("id")
            return _result