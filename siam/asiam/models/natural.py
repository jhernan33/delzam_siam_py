from django.contrib.postgres.fields import JSONField
from .base import Base
from django.db import models


class Natural(Base):
    naci_pena = models.CharField    ('Nacionalidad',         max_length=10, null=True, blank=True, default='')
    cedu_pena = models.IntegerField ('Cedula',               null=False, blank=False, default=0, unique=True)
    prno_pena = models.CharField    ('Primer Nombre',        max_length=50, null=False, blank=False, default='')
    seno_pena = models.CharField    ('Segundo Nombre',       max_length=50, null=True, blank=True, default='')
    prap_pena = models.CharField    ('Primer Apellido',      max_length=50, null=False, blank=False, default='')
    seap_pena = models.CharField    ('Segundo Apellido',     max_length=50, null=True, blank=True, default='')
    sexo_pena = models.CharField    ('Sexo',                 max_length=10, null=False, blank=False, default='')
    edoc_pena = models.CharField    ('Estado Civil',         max_length=10, null=True, blank=True, default='')
    fena_pena = models.DateField    ('Fecha de Nacimiento', blank=True, null=True,auto_now=False, auto_now_add=False)
    dire_pena = models.TextField    ('Direccion Habitacion', max_length=254, null=True, blank=True, default='')
    riff_pena = models.CharField    ('RIF',                  max_length=15, null=True, blank=True, default='')
    codi_ciud = models.ForeignKey(
        'Ciudad',
        on_delete=models.CASCADE,
        related_name='natural.codi_ciud+',
    )
    codi_sect = models.ForeignKey(
        'Sector',
        on_delete=models.CASCADE,
        related_name='natural.codi_sect+',
    )

    def nomb_apel(self):
        return '%s %s %s %s' % (self.prno_pena, self.seno_pena, self.prap_pena, self.seap_pena)

    def nombre_completo(self):
        return '%s %s' % (self.prno_pena, self.seno_pena)

    def apellido_completo(self):
        return '%s %s' % (self.prap_pena, self.seap_pena) 

    def rifc_pena (self):
        return '%s %s %s' % (self.naci_pena, self.cedu_pena, self.riff_pena) 


    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"natural"'
    
    def get_queryset():
        return Natural.objects.all().filter(deleted__isnull=True)

    # Restore Id Deleted
    def restoreNatural(key):
        # natural = Natural.objects.get(pk=key)
        # natural.deleted = None
        # natural.save()
        Natural.objects.filter(id=key).update(deleted =None)
    
    def validate_codi_natu(value):
        queryset = Natural.objects.filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True