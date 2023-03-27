from .base import Base
from django.db import models

class Zona(Base):
    desc_zona = models.CharField    ('Nombre de la Zona', max_length=200, null=False, blank=False, default='', unique=True)
    orde_zona = models.IntegerField ('Ordenamiento de la Zona',null=True, blank=True)
    
    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"zona"'

    def save(self, **kwargs):
        self.desc_zona = self.desc_zona.upper()
        return super().save(**kwargs)

    def get_queryset():
        return Zona.objects.all().filter(deleted__isnull=True)
    
    """ Get Instance Zona """
    def getInstanceZona(Id):
        return Zona.objects.get(id = Id)
    
    """ Get All Zones """
    def getZoneFilterArray(_zoneId):
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

            _result = Zona.get_queryset().filter(id__in = _zoneList).values("desc_zona")
            all =""
            for k in _result:
                all += ","+k["desc_zona"] if len(all) > 1 else k["desc_zona"]
            
            return all