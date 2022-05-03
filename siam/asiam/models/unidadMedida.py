from .base import Base
from django.db import models
#Unidad de medida
class UnidadMedida(Base):
    desc_unme = models.CharField    ('Descripcion',    max_length=50, null=False, blank=False, default='', unique=True)

    class Meta:
        ordering = ['desc_unme']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"unidad_medida"'
