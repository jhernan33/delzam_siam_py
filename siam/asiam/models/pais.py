from django.db import models
from .base import Base


class Pais(Base):
    nomb_pais=models.CharField   ('Nombre del Pais',    max_length=120, null=False, blank=False, default='', unique=True)
    name_pais =models.CharField  ('Nombre del Pais en Ingles', max_length=50, null=True, blank=True, default='')
    dial_pais=models.CharField   ('Prefijo Telefonico del Pais', max_length=15, null=True, blank=True, default='')
    code_pais=models.CharField   ('Codigo del Pais', max_length=15, null=True, blank=True, default='')

    class Meta:
        ordering = ['nomb_pais']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"pais"'

    def save(self, *args, **kwargs):        
        self.nomb_pais = self.nomb_pais.upper()
        self.name_pais = self.name_pais.upper()
        return super(Pais,self).save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Familia."""
        return self.nomb_pais, self.name_pais.upper()
