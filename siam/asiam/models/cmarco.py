from .base import Base
from django.db import models
#contrato marco
class Cmarco(Base):
    fech_coma=models.DateField    ('Fecha')
    nome_coma=models.CharField    ('Nombre',    max_length=120, null=True, blank=True, default='', unique=True)
    desc_coma=models.TextField    ('Descripcion',    max_length=1, null=True, blank=True, default='')

    class Meta:
        ordering = ['fech_coma']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"cmarco"'
