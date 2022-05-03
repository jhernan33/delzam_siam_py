from .base import Base
from django.db import models

class SubCategoria(Base):
    nomb_suca=models.CharField    ('Nombre de la Categoria',    max_length=120, null=True, blank=True, default='', unique=True)
    codi_cate = models.ForeignKey(
        'Categoria',
        on_delete=models.CASCADE,
        related_name='Categoria',
    )
    

    class Meta:
        ordering = ['nomb_suca']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"subcategoria"'
