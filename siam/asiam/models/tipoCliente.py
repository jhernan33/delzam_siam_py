from .base import Base
from django.db import models
#Tipo de clientes
class Tipocliente(Base):
    desc_ticl = models.CharField    ('Descripcion del Tipo de Cliente',    max_length=120, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_ticl']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"tipo_cliente"'
