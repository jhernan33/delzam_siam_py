from .base import Base
from django.db import models

class Contacto(Base):
    desc_cont = models.CharField ('Descripcion del Contacto', max_length=200, null=False, blank=False)
    codi_grco = models.ForeignKey('GrupoCategoriaContacto',
        on_delete=models.CASCADE,
        related_name='GrupoCategoriaContacto')
    codi_clie = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='contacto_cliente_codi_clie'
        ,null=True, blank=True
    )
    codi_prov = models.ForeignKey(
        'Proveedor',
        on_delete=models.CASCADE,
        related_name='contacto_proveedor_codi_prov'
        ,null=True, blank=True
    )
    codi_vend = models.ForeignKey(
        'Vendedor',
        on_delete=models.CASCADE,
        related_name='contacto_vendedor_codi_vend'
        ,null=True, blank=True
    )
    codi_natu = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='contacto_natural_codi_natu'
        ,null=True, blank=True
    )
    codi_juri = models.ForeignKey(
        'Juridica',
        on_delete=models.CASCADE,
        related_name='contacto_juridica_codi_juri'
        ,null=True, blank=True
    )
    codi_acci = models.ForeignKey(
        'Accionista',
        on_delete=models.CASCADE,
        related_name='contacto_accionista_codi_acci'
        ,null=True, blank=True
    )

    class Meta:
        ordering = ['-id']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"comun\".\"contacto"'

    def save(self, **kwargs):
        self.desc_cont = self.desc_cont.lower()
        return super().save(**kwargs)

    def get_queryset():
        return Contacto.objects.all().filter(deleted__isnull=True)
    
    # Check Contact
    def check_contact(desc_cont,codi_grou):
        queryset = Contacto.get_queryset().filter(desc_cont = str(desc_cont).strip().lower()).filter(codi_grco_id = codi_grou)
        if queryset.count() == 0:
            return False
        else:
            return True
    
    def delete_contact(codi_eval,id):
        if str(codi_eval).strip() =='codi_natu':
            Contacto.objects.filter(codi_natu = id).delete()
        elif str(codi_eval).strip() =='codi_juri':
            Contacto.objects.filter(codi_juri = id).delete()
