from .base import Base
from django.db import models
#Forma de pago
class FormaPago(Base):
    desc_fopa=models.CharField    ('Descripcion de la Forma de Pago',    max_length=120, null=True, blank=True, default='', unique=True)

    class Meta:
        ordering = ['desc_fopa']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"forma_pago"'
