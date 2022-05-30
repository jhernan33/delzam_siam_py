from datetime import datetime
from .base import Base
from django.db import models
#Tipo de empresas
class TipoEmpresa(Base):
    desc_tiem=models.CharField    ('Descricpcion tipo de empresa',    max_length=30, null=False, blank=False, default='', unique=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"tipo_empresa"'

    def save(self, **kwargs):
        self.desc_tiem = self.desc_tiem.upper()
        return super().save(**kwargs)
