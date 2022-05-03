from .base import Base
from django.db import models
#Forma de pago
class Fpago(Base):
    desc_fopa=models.CharField    ('Descripcion',    max_length=40, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_fopa']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"fpago"'
