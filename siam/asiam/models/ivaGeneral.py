from .base import Base
from django.db import models

class IvaGeneral(Base):
    desc_ivag = models.CharField  ('Descripcion del Iva General', max_length=120,null=True, blank=True, unique=True)
    
    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"iva_general"'
    
    def save(self, *args, **kwargs):        
        self.desc_ivag = self.desc_ivag.upper()
        return super(IvaGeneral,self).save(*args, **kwargs)

    def get_queryset():
        return IvaGeneral.objects.all().filter(deleted__isnull=True)
