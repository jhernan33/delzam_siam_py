from .base import Base
from django.db import models
#Grado de instruccion
class Ginstruccion(Base):
    desc_grin=models.CharField    ('Descripcion',    max_length=50, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_grin']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"ginstruccion"'
