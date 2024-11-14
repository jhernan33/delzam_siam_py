from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField

class Vendedor(Base):
    fein_vend = models.DateField  ('Fecha de Ingreso del Vendedor',auto_now=False, auto_now_add=False)
    foto_vend = models.JSONField  ('Foto del Vendedor',null=True, blank=True)
    codi_natu = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='natural',
    )
    # lice_vend = models.BooleanField('Poseee Licencia S/N',null=True, blank=True)
    # grli_vend = models.CharField('Grado de Licencia', max_length=250, null=True, blank=True, default='')
    # crtm_vend = models.CharField('Certificado Medico', max_length=250, null=True, blank=True, default='')
    
    class Meta:
        ordering = ['codi_natu']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"vendedor"'

    def get_queryset():
        return Vendedor.objects.all().filter(deleted__isnull=True)
    
    def validate_codi_natu(data,key):
        queryset = Vendedor.objects.filter(codi_natu = data['codi_natu'])
        if queryset.count() == 0:
            return True
        else:
            # Check id 
            if queryset[0].id == key:
                return True
            else:
                return False
    
    """ Is Seller """
    def isSeller(Id):
        resultQuerySetSeller = Vendedor.get_queryset().filter(codi_natu = Id)
        return False if resultQuerySetSeller.count() <= 0 else True
    
    def getSeller(_sellerId):
        if isinstance(_sellerId,str):
            # Create List
            _sellerList = []
            ocu_pri = 0
            # Check Count Ocurrences
            indexes = [i for i, c in enumerate(_sellerId) if c ==',']
            if len(indexes) >0:
                # Iterate Indexes
                for x in indexes:
                    if ocu_pri == 0:
                        _sellerList.append(int(_sellerId[ocu_pri:x]))
                        ocu_pri = x
                    elif ocu_pri > 0:
                        _sellerList.append(int(_sellerId[ocu_pri+1:x]))
                        ocu_pri = x
                _sellerList.append(int(_sellerId[ocu_pri+1:len(_sellerId)]))
            elif len(indexes) ==0:
                _sellerList.append(int(_sellerId[0:len(_sellerId)]))
            
            return _sellerList