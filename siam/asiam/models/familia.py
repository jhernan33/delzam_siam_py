from .base import Base
from django.db import models

class Familia(Base):
    desc_fami=models.CharField ('desc_fami',   max_length=200, null=False, blank=False, default='', unique=True)
    abae_fami=models.CharField ('abae_fami',   max_length=3, null=True, blank=True, default='', unique=True)
    agru_fami=models.CharField ('agru_fami',   max_length=1, null=True, blank=True, default='')

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"familia"'

    def save(self, *args, **kwargs):        
        self.desc_fami = self.desc_fami.upper()
        self.abae_fami = self.abae_fami.upper()
        return super(Familia,self).save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Familia."""
        return self.desc_fami, self.abae_fami.upper()