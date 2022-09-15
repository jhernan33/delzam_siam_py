from .base import Base
from django.db import models

class CategoriaContacto(Base):
    desc_ctco = models.CharField    ('Descripcion de la Categoria del Contacto', max_length=200, null=False, blank=False, default='', unique=True)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"categoria_contacto"'

    def save(self, **kwargs):
        self.desc_ctco = self.desc_ctco.upper()
        return super().save(**kwargs)

    def get_queryset():
        return CategoriaContacto.objects.all().filter(deleted__isnull=True)