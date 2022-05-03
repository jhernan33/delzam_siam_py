from django.db import models
from .base import Base

class Estado(Base):
    nomb_esta = models.CharField    ('Nombre del Estado',    max_length=30, null=False, blank=False, default='', unique=True)
    codi_pais = models.ForeignKey(
        'Pais',
        on_delete=models.CASCADE,
        related_name='Pais',
    )

    class Meta:
        ordering = ['nomb_esta']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"estado"'

    def save(self, *args, **kwargs):
        self.nomb_esta = self.nomb_esta.upper()
        return super(Estado,self).save(*args, **kwargs)