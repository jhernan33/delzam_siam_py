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

            #_result = Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona').all()
            # from asiam.models import Cliente
            #_result = Cliente.objects.filter(ruta_detalle_vendedor_cliente__in = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in =Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona'))).order_by('id')
            #_result = Ruta.get_queryset().prefetch_related('rutadetallevendedor').filter(codi_zona__in = _zoneList).select_related('codi_zona')
            #_result = Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona')

            # use Raw
            ## _result = Ruta.objects.raw("select zona.id,zona.desc_zona,zona.orde_zona,ruta.nomb_ruta,ruta.id,ruta.posi_ruta,deta_ruta.id,clie.codi_ante,clie.codi_natu_id,clie.codi_juri_id from empr.zona as zona join empr.ruta as ruta on ruta.codi_zona_id = zona.id join empr.ruta_detalle_vendedor as deta_ruta on deta_ruta.codi_ruta_id = ruta.id join empr.cliente as clie on ruta_detalle_vendedor_cliente_id = deta_ruta.id where zona.id in(%s) order by zona.orde_zona,ruta.posi_ruta",[_zoneList])
            
            # cursor = connection.cursor()
            # cursor.execute('''select zona.id,zona.desc_zona,zona.orde_zona from empr.zona as zona order by zona.orde_zona''')
            # _result = cursor.fetchall

            _result = Ruta.objects.raw('''select zona.id,zona.desc_zona,zona.orde_zona,ruta.nomb_ruta,ruta.id,ruta.posi_ruta,deta_ruta.id,clie.codi_ante,clie.codi_natu_id,clie.codi_juri_id from empr.zona as zona join empr.ruta as ruta on ruta.codi_zona_id = zona.id join empr.ruta_detalle_vendedor as deta_ruta on deta_ruta.codi_ruta_id = ruta.id join empr.cliente as clie on ruta_detalle_vendedor_cliente_id = deta_ruta.id where zona.id in(%s) order by zona.orde_zona,ruta.posi_ruta''',[_zoneList])

            # _result = Zona.get_queryset().filter(id__in = _zoneList).select_related('Ruta')
            # _result = RutaDetalleVendedor.get_queryset().filter(codi_ruta__in = Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona').all())
            # _result = Ruta.get_queryset().filter(codi_zona__in = _zoneList).select_related('codi_zona').all()
            return _result