from .base import Base
from django.db import models

class GrupoCategoriaContacto(Base):
    desc_grup = models.CharField ('Descripcion del Grupo de la Categoria del Contacto', max_length=200, null=False, blank=False)
    codi_ctco = models.ForeignKey('CategoriaContacto',
        on_delete=models.CASCADE,
        related_name='CategoriaContacto',)

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"grupo_categoria_contacto"'
        unique_together = ('desc_grup','codi_ctco')

    def save(self, **kwargs):
        self.desc_grup = self.desc_grup.upper()
        return super().save(**kwargs)

    def get_queryset():
        return GrupoCategoriaContacto.objects.all().filter(deleted__isnull=True)