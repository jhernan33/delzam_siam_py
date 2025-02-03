import os
from typing import List
from rest_framework import serializers
from asiam.models import Cliente, Vendedor, Natural, Juridica, RutaDetalleVendedor, Contacto, Pedido
from asiam.serializers import NaturalSerializer,JuridicaSerializer,VendedorSerializer
from asiam.serializers.rutaDetalleVendedorSerializer import RutaDetalleVendedorSerializer
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_gis.serializers import GeoFeatureModelListSerializer
from django.db.models import Sum

# import datetime module
from datetime import datetime


class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        if isinstance(value, list):
            place = settings.WEBSERVER_IMAGES
            enviromentArticle = os.path.realpath(settings.WEBSERVER_CUSTOMER)[1:]+'/'
            for obj in value:
                obj['image'] = place+enviromentArticle+obj['image']
            return value

    def to_internal_value(self, data):
        return data

class ClienteSerializer(serializers.ModelSerializer):
#class ClienteSerializer(GeoFeatureModelListSerializer):
    # codi_vend = VendedorSerializer()
    ruta_detalle_vendedor_cliente = RutaDetalleVendedorSerializer()
    codi_natu = NaturalSerializer()
    codi_juri = JuridicaSerializer()
    foto_clie = JSONSerializerField()

    class Meta:
        model = Cliente
        field = ('id','fein_clie','codi_ante','cred_clie','mocr_clie','plcr_clie'
        ,'prde_clie','prau_clie','codi_natu','codi_juri','foto_clie','obse_clie','deleted','ruta_detalle_vendedor_cliente','ptor_clie')
        exclude =['created','updated','esta_ttus']
        geo_field = "location_clie"
        # auto_bbox = True # Ubckyd
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['codi_ante'] = str(instance.codi_ante).upper()
        # Customer all
        representation['customer_all'] = Cliente.searchTypeCustomerId(instance.id)
        representation['customer_address'] = Cliente.searchAddressCustomer(instance.id)
        # Detail Orders
        from asiam.serializers import PedidoSerializer
        queryset_details = Pedido.get_queryset().filter(codi_clie = instance.id)
        result_details = PedidoSerializer(queryset_details, many=True).data
        representation['customer_sales_history'] = {
            'total_orders' : Pedido.get_queryset().filter(codi_clie = instance.id).count(),
            # State 2 and 7 
            'total_paid_orders': Pedido.get_queryset().filter(codi_clie = instance.id).filter(codi_espe__in = (2,7)).count(),
            'total_outstanding_orders': Pedido.get_queryset().filter(codi_clie = instance.id).filter(codi_espe = 1).count(),
            'total_debt' : Pedido.get_queryset().filter(codi_clie = instance.id).filter(codi_espe = 7).aggregate(tota_pedi=Sum('tota_pedi'))['tota_pedi'] if Pedido.get_queryset().filter(codi_clie = instance.id).filter(codi_espe = 7).count()>0 else 0,
            # Date of last sale
            'date_of_last_sale': datetime.strftime(Pedido.get_queryset().filter(codi_clie = instance.id).order_by('-created').values('created')[:1][0]['created'],"%d-%m-%Y %H:%M:%S")  if Pedido.get_queryset().filter(codi_clie = instance.id).count() > 0 else '',
            'Details' : {"data":result_details}  # Return Dictionary
        }
        return representation
    
    def validate_codi_vend(value):
        queryset = RutaDetalleVendedor.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True

    def validate_codi_natu(value,state):
        queryset = Natural.objects.filter(id = value) if state else Natural.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True    
    
    def validate_codi_juri(value,state):
        queryset = Juridica.objects.filter(id = value) if state else Juridica.get_queryset().filter(id = value)
        if queryset.count() == 0:
            return False
        else:
            return True

class ClienteComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        field = ['id','description']
        exclude = ['created','updated','esta_ttus','codi_natu','fein_clie','codi_ante','cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie','obse_clie','deleted','ruta_detalle_vendedor_cliente','ptor_clie','location_clie','codi_juri','posi_clie']

    def to_representation(self, instance):
        data = super(ClienteComboSerializer, self).to_representation(instance=instance)
        
        # Add Description for Natural or Juridica
        _description = Cliente.searchCustomerId(instance.id)
        data["description"] = _description
        return data
    
class ClienteBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        field = ('id','codi_natu')
        exclude = ['created','updated','esta_ttus','fein_clie','codi_ante','cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie','obse_clie','deleted','ruta_detalle_vendedor_cliente','ptor_clie','location_clie','codi_juri','posi_clie']

class ClienteRutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        field = ('id','posi_clie','codi_ante','description')
        exclude = ['created','updated','esta_ttus','fein_clie','cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie','obse_clie','deleted','ruta_detalle_vendedor_cliente','ptor_clie','location_clie','codi_juri','codi_natu']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Add Description for Natural or Juridica
        _description = Cliente.searchCustomerId(instance['id'])
        representation["description"] = _description
        return representation

"""
    Report Custom Screen
"""
class ClienteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        field = ('id','codi_ante','description','codi_natu','codi_juri','location_clie')
        exclude = ['created','updated','deleted','esta_ttus','fein_clie','cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie','obse_clie','ptor_clie','posi_clie']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Add Description Seller
        _result_seller =  RutaDetalleVendedor.searchSeller(instance.ruta_detalle_vendedor_cliente)
        _descriptionSeller = _result_seller

        # Add Description for Natural or Juridica
        _description = Cliente.searchTypeCustomerId(instance.id)
        representation["description_customer"] = _description+" (Vend.) "+_descriptionSeller

        # Add Contact for Customer c
        _contact = Contacto.search_contact(instance.id)
        representation["contact"] = _contact

        # Add Adress for Customer Contacto
        _address = Cliente.searchAddressCustomer(instance.id)
        representation["address"] = _address

        return representation


class ClienteReportExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        field = ('id','codi_ante','description','ruta_detalle_vendedor_cliente','location_clie')
        exclude = ['created','updated','deleted','esta_ttus','codi_juri','codi_natu','fein_clie','cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie','obse_clie','ptor_clie','posi_clie']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        for obj in instance:
            _result_detail = RutaDetalleVendedor.objects.filter(id = obj['ruta_detalle_vendedor_cliente_id']).values("codi_vend")
            _result_seller = Vendedor.objects.filter(id = _result_detail[0]['codi_vend']).values('codi_natu')
            _result_natural = Natural.objects.filter(id = _result_seller[0]['codi_natu'])
            _description = str(_result_natural[0].prno_pena[0]+"."+_result_natural[0].seno_pena[0]+"."+_result_natural[0].prap_pena[0]+"."+_result_natural[0].seap_pena[0]).strip().upper()

            # Add Description for Natural or Juridica
            # _description = Cliente.searchTypeCustomerId(instance.id)

            _resultClient = Cliente.objects.filter(id = obj['id']).values('id','codi_natu','codi_juri')
            _descriptionCustomer = ""

            for customer in _resultClient:
                if customer['codi_natu'] != 1:
                    _resultQuerySet = Natural.objects.filter(id = customer['codi_natu'])
                    for natural in _resultQuerySet:
                        _descriptionCustomer = str(str(natural.cedu_pena)+" / "+natural.prno_pena+ ' '+natural.seno_pena+' '+natural.prap_pena+' '+ natural.seap_pena).strip().upper()+" (N)"
                else:
                    _resultQuerySet = Juridica.objects.filter(id = customer['codi_juri'])
                    for juridica in _resultQuerySet:
                        _descriptionCustomer = str(juridica.riff_peju+" / "+juridica.raso_peju).strip().upper()+" (J)"
            obj['description_customer'] = _description+" (Vend.) "+_descriptionCustomer
        
        return representation

class ClienteBuscarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        field = ['id','codi_ante','ptor_clie','ruta_detalle_vendedor_cliente']
        exclude =['created','updated','esta_ttus','location_clie','fein_clie','cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie','obse_clie','codi_natu','codi_juri','deleted','posi_clie']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['codi_ante'] = str(instance.codi_ante).upper()
        # Customer all
        representation['customer_all'] = Cliente.searchTypeCustomerId(instance.id)
        return representation

class HistoryCustomerSerializer(serializers.ModelSerializer):
    codeCustomer  = serializers.SerializerMethodField("get_code_customer")
    customerName  = serializers.SerializerMethodField("get_customer_name")
    zone   = serializers.SerializerMethodField("get_zone")
    route  = serializers.SerializerMethodField("get_route")
    seller = serializers.SerializerMethodField("get_seller")
    lastVisitDate = serializers.SerializerMethodField("get_last_Visit_Date")
    status = serializers.SerializerMethodField("get_Status")
    address = serializers.SerializerMethodField("get_address")
    contact = serializers.SerializerMethodField("get_contact")

    class Meta:
        model = Cliente
        field = (
            
            'zone'
            ,'route'
            ,'seller'
            ,'lastVisitDate'
            ,'location_clie'
            )
        exclude = [
            'id','created','updated','deleted','esta_ttus','fein_clie'
            ,'cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie'
            ,'obse_clie','ptor_clie','posi_clie','codi_ante'
            ,'ruta_detalle_vendedor_cliente','codi_natu','codi_juri'
            ]
        # fields = '__all__'
    def get_customer_name(self,obj):
        fullName = None
        if obj is not None and isinstance(obj, bytes)== False:
            fullName = (
                    obj.codi_ante
                    + " / "
                    + obj.codi_natu.riff_pena
                    + " / "
                    + " " +obj.codi_natu.prno_pena
                    + " "+obj.codi_natu.seno_pena
                    + " "+obj.codi_natu.prap_pena
                    + " "+obj.codi_natu.seap_pena 
                    +" (N)" if obj.codi_natu.id != 1 else 
                    obj.codi_ante
                    + " / "
                    + str(obj.codi_juri.riff_peju)+" "+str(obj.codi_juri.raso_peju).strip().upper()+" (J)"
                    
            )
        return fullName
    
    def get_seller(self,obj):
        seller = None
        if obj is not None and isinstance(obj, bytes)== False:
            seller =  (
                obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.prno_pena
                + " "+obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.seno_pena
                + " "+obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.prap_pena
                + " "+obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.seap_pena
                )
        return seller
    
    def get_zone(self,obj):
        zone = None 
        if obj is not None and isinstance(obj, bytes)== False:
            zone =obj.ruta_detalle_vendedor_cliente.codi_ruta.codi_zona.desc_zona
        return zone
    
    def get_route(self,obj):
        route = None
        if obj is not None and isinstance(obj, bytes)== False:
            route = obj.ruta_detalle_vendedor_cliente.codi_ruta.nomb_ruta
        return route
    
    def get_code_customer(self,obj):
        code = None
        if obj is not None and isinstance(obj, bytes)== False:
            code = obj.codi_ante
        return code

    def get_last_Visit_Date(self,obj):
        resultVisit = None
        if obj is not None and isinstance(obj, bytes)== False:
            resultVisit = obj.Visit
            from datetime import datetime
            if resultVisit is not None:
                resultVisit = resultVisit.strftime("%d-%m-%Y")
        return resultVisit if resultVisit is not None else str('').strip()

    def get_Status(self,obj):
        days = None
        days = self.context.get('request').query_params.get('days',None)
        if days is not None:
            if obj is not None and isinstance(obj, bytes)== False:
                resultVisit = obj.Visit
                from datetime import datetime,timedelta
                if resultVisit is not None:
                    days = int(days)
                    diferenceDays = datetime.today().date() - resultVisit
                    if diferenceDays.days <= days:
                        return 'Ultima compra fue hace '+str(diferenceDays.days)+' Días'
                    else:
                        return 'Disponible'
        return "Disponible"
    
    def get_address(self,obj):
        fullAddress = None
        if obj is not None and isinstance(obj, bytes)== False:
            fullAddress = (
                str(obj.codi_natu.codi_sect.nomb_sect)
                    + " "+str(obj.codi_natu.codi_ciud.nomb_ciud)
                    + " "+str(obj.codi_natu.dire_pena)
                    if obj.codi_natu.id != 1 else 
                    str(obj.codi_juri.codi_sect.nomb_sect)
                    +" "+str(obj.codi_juri.codi_ciud.nomb_ciud)+str(obj.codi_juri.dofi_peju)
            )
        return fullAddress
    
    def get_contact(self,obj):
        fullContact = None
        if obj is not None and isinstance(obj, bytes)== False:
            fullContact = obj.Contact_Natural if obj.codi_natu.id != 1 else  obj.Contact_Legal
        return fullContact


class HistoryCustomerReportSerializer(serializers.ModelSerializer): 
    codeCustomer  = serializers.SerializerMethodField("get_code_customer")
    customerName  = serializers.SerializerMethodField("get_customer_name")
    zone   = serializers.SerializerMethodField("get_zone")
    route  = serializers.SerializerMethodField("get_route")
    seller = serializers.SerializerMethodField("get_seller")
    lastVisitDate = serializers.SerializerMethodField("get_last_Visit_Date")
    status = serializers.SerializerMethodField("get_Status")
    address = serializers.SerializerMethodField("get_address")
    contact = serializers.SerializerMethodField("get_contact")
    coordinates = serializers.SerializerMethodField("get_coordinates")

    class Meta:
        model = Cliente
        field = (
            
            'zone'
            ,'route'
            ,'seller'
            ,'lastVisitDate'
            # ,'location_clie'
            ,'coordinates'
            )
        exclude = [
            'id','created','updated','deleted','esta_ttus','fein_clie'
            ,'cred_clie','mocr_clie','plcr_clie','prde_clie','prau_clie','foto_clie'
            ,'obse_clie','ptor_clie','posi_clie','codi_ante'
            ,'ruta_detalle_vendedor_cliente','codi_natu','codi_juri'
            ]
        
    def get_coordinates(self,obj):
        _coordinates = None
        if obj is not None and isinstance(obj, bytes)== False:
            _coordinates = obj.location_clie
            _coordinates = " ".join(str(_coordinates.x).split())+" "+" , ".join(str(_coordinates.y).split())
        return _coordinates
    
    def get_customer_name(self,obj):
        fullName = None
        if obj is not None and isinstance(obj, bytes)== False:
            fullName = (
                    obj.codi_ante
                    + " / "
                    + obj.codi_natu.riff_pena
                    + " / "
                    + " " +obj.codi_natu.prno_pena
                    + " "+obj.codi_natu.seno_pena
                    + " "+obj.codi_natu.prap_pena
                    + " "+obj.codi_natu.seap_pena 
                    +" (N)" if obj.codi_natu.id != 1 else 
                    obj.codi_ante
                    + " / "
                    + str(obj.codi_juri.riff_peju)+" "+str(obj.codi_juri.raso_peju).strip().upper()+" (J)"
                    
            )
        return fullName
    
    def get_seller(self,obj):
        seller = None
        if obj is not None and isinstance(obj, bytes)== False:
            seller =  (
                obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.prno_pena
                + " "+obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.seno_pena
                + " "+obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.prap_pena
                + " "+obj.ruta_detalle_vendedor_cliente.codi_vend.codi_natu.seap_pena
                )
        return seller
    
    def get_zone(self,obj):
        zone = None 
        if obj is not None and isinstance(obj, bytes)== False:
            zone =obj.ruta_detalle_vendedor_cliente.codi_ruta.codi_zona.desc_zona
        return zone
    
    def get_route(self,obj):
        route = None
        if obj is not None and isinstance(obj, bytes)== False:
            route = obj.ruta_detalle_vendedor_cliente.codi_ruta.nomb_ruta
        return route
    
    def get_code_customer(self,obj):
        code = None
        if obj is not None and isinstance(obj, bytes)== False:
            code = obj.codi_ante
        return code

    def get_last_Visit_Date(self,obj):
        resultVisit = None
        if obj is not None and isinstance(obj, bytes)== False:
            resultVisit = obj.Visit
            from datetime import datetime
            if resultVisit is not None:
                resultVisit = resultVisit.strftime("%d-%m-%Y")
        return resultVisit if resultVisit is not None else str('').strip()

    def get_Status(self,obj):
        days = obj.Days
        if days is not None:
            if obj is not None and isinstance(obj, bytes)== False:
                resultVisit = obj.Visit
                from datetime import datetime,timedelta
                if resultVisit is not None:
                    days = int(days)
                    diferenceDays = datetime.today().date() - resultVisit
                    if diferenceDays.days <= days:
                        return 'Ultima compra fue hace '+str(diferenceDays.days)+' Días'
                    else:
                        return 'Disponible'
        return "Disponible"
    
    def get_address(self,obj):
        fullAddress = None
        if obj is not None and isinstance(obj, bytes)== False:
            fullAddress = (
                str(obj.codi_natu.codi_sect.nomb_sect)
                    + " "+str(obj.codi_natu.codi_ciud.nomb_ciud)
                    + " "+str(obj.codi_natu.dire_pena)
                    if obj.codi_natu.id != 1 else 
                    str(obj.codi_juri.codi_sect.nomb_sect)
                    +" "+str(obj.codi_juri.codi_ciud.nomb_ciud)+str(obj.codi_juri.dofi_peju)
                    
            )
        return fullAddress
    
    def get_contact(self,obj):
        fullContact = None
        if obj is not None and isinstance(obj, bytes)== False:
            fullContact = obj.Contact_Natural if obj.codi_natu.id != 1 else  obj.Contact_Legal
        return fullContact
