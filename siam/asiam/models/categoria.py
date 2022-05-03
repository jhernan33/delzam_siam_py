from .base import Base
from django.db import models

class Categoria(Base):
    desc_cate=models.CharField    ('Nombre de la Categoria',    max_length=120, null=True, blank=True, default='', unique=True)
    

    class Meta:
        ordering = ['desc_cate']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"categoria"'
