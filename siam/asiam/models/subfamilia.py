from .base import Base
from django.db import models

class SubFamilia(Base):
    desc_sufa = models.CharField ('desc_sufa',   max_length=200, null=False, blank=False, default='', unique=True)
    abae_sufa = models.CharField ('abae_sufa',   max_length=3, null=True, blank=True, default='', unique=True)
    agru_sufa = models.CharField ('agru_sufa',   max_length=1, null=True, blank=True, default='')
    codi_fami = models.ForeignKey(
        'Familia',
        on_delete=models.CASCADE,
        related_name='Familia',
    )

    class Meta:
        ordering = ['desc_sufa']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"sub_familia"'

    def save(self, *args, **kwargs):        
        self.desc_sufa = self.desc_sufa.upper()        
        return super(SubFamilia,self).save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Familia."""
        return self.desc_sufa