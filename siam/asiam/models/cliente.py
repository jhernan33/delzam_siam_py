from .base import Base
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models
from asiam.models.rutaDetalleVendedor import RutaDetalleVendedor
from asiam.models import Juridica, Natural

class Cliente(Base):
    fein_clie = models.DateField  ('Fecha de Ingreso del Cliente',auto_now=False, auto_now_add=False,blank=True, null=True)
    codi_ante = models.CharField    ('Codigo Anterior', max_length=75, null=True, blank=True)
    cred_clie = models.BooleanField('Credito del Cliente')
    mocr_clie = models.DecimalField ('Monto del Credito',max_digits=7,decimal_places=2)
    plcr_clie = models.IntegerField ('Plazo del del Credito')
    prde_clie = models.DecimalField ('Porcentage de Descuento',max_digits=7,decimal_places=2)
    prau_clie = models.DecimalField ('Porcentage de Aumento',max_digits=7,decimal_places=2)

    codi_natu = models.ForeignKey(
        'Natural',
        on_delete=models.CASCADE,
        related_name='natural.codi_natu+'
    )
    codi_juri = models.ForeignKey(
        'Juridica',
        on_delete=models.CASCADE,
        related_name='Juridica.codi_juri+'
    )
    foto_clie = models.JSONField  ('Foto del Cliente',null=True, blank=True)
    obse_clie = models.TextField('Observaciones del Cliente',null=True, blank=True)
    posi_clie = models.IntegerField('Posicion del Cliente para la Entrega',null=True, blank=True)
    location_clie = models.PointField(srid=4326, null=True, blank=True)
    ruta_detalle_vendedor_cliente = models.ForeignKey(RutaDetalleVendedor, on_delete=models.CASCADE, null= True)
    ptor_clie = models.TextField('Punto de Referencia del Cliente',null=True, blank=True)
    
    class Meta:
        ordering = ['codi_natu']
        indexes  = [models.Index(fields=['id',])] 
        db_table = u'"empr\".\"cliente"'

    def get_queryset():
        return Cliente.objects.all().filter(deleted__isnull=True)
    
    """ Get Search Array Customer """
    def searchCustomerArray(_arrayCustomer):
        arrayCustomer = []
        # Buscar las personas Naturales
        queryset = Cliente.objects.filter(id__in =_arrayCustomer).exclude(codi_natu=1)
        for customer in queryset:
            arrayCustomer.append(customer.id)
        _resultNatural = Natural.searchNaturalArray(arrayCustomer)
        return _resultNatural

    """     Search Customer for Id     """
    def searchCustomerId(_id):
        _resultClient = Cliente.objects.filter(id = _id).values('id','codi_natu','codi_juri')
        _descriptionCustomer = ""
        for customer in _resultClient:
            if customer['codi_natu'] != 1:
                _resultQuerySet = Natural.objects.filter(id = customer['codi_natu'])
                for natural in _resultQuerySet:
                    _descriptionCustomer = str(natural.prno_pena+ ' '+natural.seno_pena+' '+natural.prap_pena+' '+ natural.seap_pena).strip().upper()
            else:
                _resultQuerySet = Juridica.objects.filter(id = customer['codi_juri'])
                for juridica in _resultQuerySet:
                    _descriptionCustomer = str(juridica.raso_peju).strip().upper()
            return _descriptionCustomer

    # Search Type of Customer
    def searchTypeCustomerId(_id):
        _resultClient = Cliente.objects.filter(id = _id).values('id','codi_natu','codi_juri','codi_ante','ptor_clie')
        _descriptionCustomer = ""
        for customer in _resultClient:
            if customer['codi_natu'] != 1:
                _resultQuerySet = Natural.objects.filter(id = customer['codi_natu'])
                for natural in _resultQuerySet:
                    _descriptionCustomer = str(customer['codi_ante']+" / "+natural.riff_pena+" / "+natural.prno_pena+ ' '+natural.seno_pena+' '+natural.prap_pena+' '+ natural.seap_pena).strip().upper()+" (N)"+ " Firma Personal: "+str(natural.razo_natu).strip().upper()
            else:
                _resultQuerySet = Juridica.objects.filter(id = customer['codi_juri'])
                for juridica in _resultQuerySet:
                    _descriptionCustomer = str(customer['codi_ante']+" / "+juridica.riff_peju+" / "+juridica.raso_peju).strip().upper()+" (J)"
            return _descriptionCustomer
    
    # Search Type Customer WithOut RIF
    def searchTypeCustomerIdWithoutRIF(_id):
        _resultClient = Cliente.objects.filter(id = _id).values('id','codi_natu','codi_juri','codi_ante')
        _descriptionCustomer = ""
        for customer in _resultClient:
            if customer['codi_natu'] != 1:
                _resultQuerySet = Natural.objects.filter(id = customer['codi_natu'])
                for natural in _resultQuerySet:
                    _descriptionCustomer = str(customer['codi_ante']+" / "+natural.prno_pena+ ' '+natural.seno_pena+' '+natural.prap_pena+' '+ natural.seap_pena).strip().upper()+" (N)"
            else:
                _resultQuerySet = Juridica.objects.filter(id = customer['codi_juri'])
                for juridica in _resultQuerySet:
                    _descriptionCustomer = str(customer['codi_ante']+" / "+juridica.raso_peju).strip().upper()+" (J)"
            return _descriptionCustomer

    # Search Adress of Customer
    def searchAddressCustomer(_id):
        _resultClient = Cliente.objects.filter(id = _id).values('id','codi_natu','codi_juri')
        _addressCustomer = "" 
        sector =""
        ciudad =""
        for customer in _resultClient:
            if customer['codi_natu'] != 1:
                _resultQuerySet = Natural.objects.filter(id = customer['codi_natu']).select_related('codi_sect').select_related('codi_ciud')
                for natural in _resultQuerySet:
                    sector = str(natural.codi_sect.nomb_sect).strip().upper() # .replace(" ","")
                    ciudad = str(natural.codi_ciud.nomb_ciud).strip().upper()
                    _addressCustomer = str(ciudad+" Sector: "+sector+" , "+natural.dire_pena).strip().upper()
            else:
                _resultQuerySet = Juridica.objects.filter(id = customer['codi_juri']).select_related('codi_sect').select_related('codi_ciud')
                for juridica in _resultQuerySet:
                    sector = str(juridica.codi_sect.nomb_sect).strip().upper()
                    ciudad = str(juridica.codi_ciud.nomb_ciud).strip().upper()
                    _addressCustomer = str(ciudad+" Sector: "+sector+" , "+juridica.dofi_peju).strip().upper()
            return _addressCustomer
    
    # Search Numbers of Phone Customer
    def searchPhoneCustomer(_id):
        from asiam.models import Contacto, CategoriaContacto
        from asiam.serializers import ContactoSoloNumeroSerializer
        result_contact = []
        contacts = ''
        _resultClient = Cliente.objects.filter(id = _id).values('id','codi_natu','codi_juri')
        for customer in _resultClient:
            if customer['codi_natu'] != 1:
                _filter = 'codi_natu'
                _value = customer['codi_natu']
            else:
                _filter = 'codi_juri'
                _value = customer['codi_juri']
            # search Contact
            _resultQueryContact = Contacto.get_queryset().filter(**{_filter:_value})
            result_contact = ContactoSoloNumeroSerializer(_resultQueryContact, many=True).data
            count = 1
            for k in result_contact:
                if count ==1:
                    contacts+= str(k['desc_cont'])
                else:
                    contacts+= ' / '+str(k['desc_cont'])
                count= count+1
            return contacts
    
    # Search City of Customer
    def searchCityCustomerId(_id):
        _resultClient = Cliente.objects.filter(id = _id).values('id','codi_natu','codi_juri')
        _cityCustomer = "" 
        sector =""
        ciudad =""
        for customer in _resultClient:
            if customer['codi_natu'] != 1:
                _resultQuerySet = Natural.objects.filter(id = customer['codi_natu']).select_related('codi_sect').select_related('codi_ciud')
                for natural in _resultQuerySet:
                    ciudad = str(natural.codi_ciud.nomb_ciud).strip().upper()
                    _cityCustomer = str(ciudad).strip().upper()
            else:
                _resultQuerySet = Juridica.objects.filter(id = customer['codi_juri']).select_related('codi_sect').select_related('codi_ciud')
                for juridica in _resultQuerySet:
                    ciudad = str(juridica.codi_ciud.nomb_ciud).strip().upper()
                    _cityCustomer = str(ciudad).strip().upper()
            return _cityCustomer

    """ Search Customer By Id 

        Returns:
            _type_: Queryset
        """
    def searchCustomerById(_id:None):
        queryset_Customer = []
        if _id is not None:
            queryset = Cliente.get_queryset().filter(id = _id)
            if queryset.count() > 0:
                queryset_Customer = queryset
        return queryset_Customer