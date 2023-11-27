from .base import Base
from django.db import models

class SubFamilia(Base):
    desc_sufa = models.CharField ('desc_sufa',   max_length=200, null=False, blank=False, default='')
    agru_sufa = models.CharField ('agru_sufa',   max_length=1, null=True, blank=True, default='')
    abae_sufa = models.CharField ('abae_sufa',   max_length=10, null=True, blank=True, default='')
    codi_fami = models.ForeignKey(
        'Familia',
        on_delete=models.CASCADE,
        related_name='Familia',
    )

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"sub_familia"'

    def save(self, *args, **kwargs):        
        self.desc_sufa = self.desc_sufa.upper()
        self.agru_sufa = self.agru_sufa.upper()
        self.abae_sufa = self.abae_sufa.upper()
        return super(SubFamilia,self).save(*args, **kwargs)

    def get_queryset():
        return SubFamilia.objects.all().filter(deleted__isnull=True)
    
    """ Get Instance SubFamilia """
    def getInstanceSubFamily(Id):
        return SubFamilia.objects.get(id = Id)