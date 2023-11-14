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
