from .base import Base
from django.db import models
#Condiciones de pago
class Cpago(Base):
    desc_copa=models.CharField    ('Descripcion',    max_length=40, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_copa']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"cpago"'
