from .base import Base
from django.db import models

class Articulo(Base):
    codi_arti = models.CharField    ('Codigo del Articulo',max_length=50, null=True, blank=True, default='', unique=True)
    idae_arti = models.CharField    ('Codigo del Articulo SIAE',max_length=15, null=True, blank=True)
    desc_arti = models.CharField    ('Nombre del Articulo',    max_length=250, null=True, blank=True, default='', unique=False)
    coba_arti = models.CharField    ('Codigo de Barras del Articulo',    max_length=30, null=True, blank=True, default='')
    cmin_arti = models.DecimalField ('Cantidad Minima',max_digits=6,decimal_places=0,null=True, blank=True)
    cmax_arti = models.DecimalField ('Cantidad Maxima',max_digits=6,decimal_places=0,null=True, blank=True)
    por1_arti = models.DecimalField ('Porcentaje de Utilidad 1 Por Articulo',max_digits=7,decimal_places=2, blank=True,default=0)
    por2_arti = models.DecimalField ('Porcentaje de Utilidad 2 Por Articulo',max_digits=7,decimal_places=2, blank=True,default=0)
    por3_arti = models.DecimalField ('Porcentaje de Utilidad 3 Por Articulo',max_digits=7,decimal_places=2, blank=True,default=0)
    por4_arti = models.DecimalField ('Porcentaje de Utilidad 4 Por Articulo',max_digits=7,decimal_places=2, blank=True,default=0)
    ppre_arti = models.DecimalField ('Porcentaje Preferido Por Articulo',max_digits=20,decimal_places=2, blank=True, default=0)
    codi_sufa = models.ForeignKey(
        'SubFamilia',
        on_delete=models.CASCADE,
        related_name='sub_familia',
    )
    foto_arti = models.JSONField('Foto del Articulo',null=True, blank=True)
    exgr_arti = models.CharField('Exento Grabado del Articulo',max_length=1, null=True, blank=True)
    codc_pres = models.ForeignKey(
        'Presentacion',
        on_delete=models.CASCADE,
        related_name='presentacion_compra',
    )
    codv_pres = models.ForeignKey(
        'Presentacion',
        on_delete=models.CASCADE,
        related_name='presentacion_venta',
    )
    capc_arti = models.IntegerField('Capacidad de Compra del Articulo',null=True, blank=True)
    capv_arti = models.IntegerField('Capacidad de Venta del Articulo',null=True, blank=True)
    proc_arti = models.CharField   ('Codigo del Articulo SIAE',max_length=1, null=True, blank=True, default='')
    codi_ivti = models.ForeignKey(
        'IvaGeneral',
        on_delete=models.CASCADE,
        related_name='ivti_general',
        blank=True, null=True
    )
    exis_arti = models.IntegerField('Existencia del Articulo',null=True, blank=True)

    class Meta:
        ordering = ['desc_arti']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"articulo"'

    def save(self, **kwargs):
        self.idae_arti = self.idae_arti.upper().strip()
        self.desc_arti = self.desc_arti.upper().strip()
        self.exgr_arti = self.exgr_arti.upper().strip() if isinstance(self.exgr_arti, str) else self.exgr_arti 
        return super(Articulo,self).save(**kwargs)

    def get_queryset():
        return Articulo.objects.all().filter(deleted__isnull=True)
    
    """ Get Instance Article """
    def getInstanceArticle(Id:int):
        return Articulo.objects.get(id = Id)
    
    '''
        Calculate Price by Code Article
    '''
    def toPriceTheProduct(code_article:int, route:int):
        _porcentage = None
        _prices = 0
        from asiam.models import Ruta
        if route is not None:
            result_route = Ruta.get_queryset().get(id = route)
            _porcentage = result_route.porc_ruta

        if code_article is not None:
            result_article = Articulo.getInstanceArticle(code_article)
            if result_article is None:
                return False
            
            if result_article is not None:
                if _porcentage is not None:
                    match _porcentage:
                        case 1:
                            _porcentage = result_article.por1_arti
                        case 2:
                            _porcentage = result_article.por2_arti
                        case 3:
                            _porcentage = result_article.por3_arti
                        case 4:
                            _porcentage = result_article.por4_arti
                
                _prices = Base.roundNumber(((result_article.ppre_arti * _porcentage)/100) + result_article.ppre_arti) if _porcentage is not None else Base.roundNumber(((result_article.ppre_arti * result_article.por1_arti)/100) + result_article.ppre_arti)
                
            return _prices
