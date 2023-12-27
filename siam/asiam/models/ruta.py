from asiam.models.rutaDetalleVendedor import RutaDetalleVendedor
from .base import Base
from django.db import models, connection
from django.db.models import Prefetch, FilteredRelation
from asiam.models import Zona

class Ruta(Base):
    codi_zona = models.ForeignKey(
        'Zona',
        on_delete=models.CASCADE,
        related_name='Zona',
    )
    nomb_ruta = models.CharField    ('Nombre de la Ruta', max_length=200, null=True, blank=True)
    posi_ruta = models.IntegerField('Posicion de la Ruta',null=True, blank=True)
    porc_ruta = models.DecimalField ('Porcentaje del Descuento de la Ruta ',max_digits=7,decimal_places=2, default=4)

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
            
            #return _zoneList
            _result = Ruta.get_queryset().filter(codi_zona__in = _zoneList).values("id")
            return _result
    

    def searchRouteFilterZone(_zoneId):
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

            _result = Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona').all()
            from asiam.models import Cliente
            _result = Cliente.objects.filter(ruta_detalle_vendedor_cliente__in = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in =Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona'))).order_by('id')
            _result = Ruta.get_queryset().prefetch_related('rutadetallevendedor').filter(codi_zona__in = _zoneList).select_related('codi_zona')
            _result = Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona')

            return _result
    
    """ Get Instance Route """
    def getInstanceRoute(Id:int):
        return Ruta.objects.get(id = Id)