from .paisSerializer import PaisSerializer, PaisBasicSerializer
from .estadoSerializer import EstadoSerializer, EstadoBasicSerializer
from .ciudadSerializer import CiudadSerializer, CiudadBasicSerializer
# # from .municipioSerializer import MunicipioSerializer
# # from .parroquiaSerializer import ParroquiaSerializer
from .sectorSerializer import SectorSerializer, SectorBasicSerializer
from .subSectorSerializer import SubSectorSerializer
from .naturalSerializer import NaturalSerializer, NaturalBasicSerializer
from .tipoempresaSerializer import TipoEmpresaSerializer
from .juridicaSerializer import JuridicaSerializer, JuridicaBasicSerializer
from .accionistaSerializer import AccionistaSerializer
from .sucursalSerializer import SucursalSerializer
from .tipoClienteSerializer import TipoClienteSerializer
from .familiaSerializer import FamiliaSerializer, FamiliaComboSerializer
from .subFamiliaSerializer import SubFamiliaSerializer, SubFamiliaComboSerializer
from .zonaSerializer import ZonaSerializer, ZonaBasicSerializer
from .vendedorSerializer import VendedorSerializer, VendedorBasicSerializer
from .rutaSerializer import RutaSerializer, RutaBasicSerializer, RutaClienteSerializer
from .unidadMedidaSerializer import UnidadMedidaSerializer
from .ivaSerializer import IvaSerializer
from .unidadTributariaSerializer import UnidadTributariaSerializer
from .clienteSerializer import ClienteSerializer, ClienteBasicSerializer, ClienteRutaSerializer, ClienteReportSerializer, ClienteReportExportSerializer, ClienteComboSerializer
from .userSerializer import SignupSerializer, UserLoginSerializer
from .grupoSerializer import GrupoSerializer
from .rutaDetalleVendedorSerializer import RutaDetalleVendedorSerializer,RutaDetalleVendedorSerializerBasics
from .ivaGeneralSerializer import IvaGeneralSerializer
from .articuloSerializer import ArticuloSerializer, ArticuloComboSerializer
from .presentacionSerializer import PresentacionSerializer
from .proveedorSerializer import ProveedorSerializer, ProveedorBasicSerializer
from .articuloProveedorSerializer import ArticuloProveedorSerializer, ArticuloProveedorSerializerBasics
from .categoriaContactoSerializer import CategoriaContactoSerializer, CategoriaContactoBasicSerializer
from .grupoCategoriaContactoSerializer import GrupoCategoriaContactoSerializer, GrupoCategoriaContactoBasicSerializer
from .contactoSerializer import ContactoSerializer, ContactoBasicSerializer
from .configuracionBusquedadSerializer import ConfiguracionBusquedadSerializer
from .pedidoTipoSerializer import PedidoTipoSerializer, PedidoTipoComboSerializer, PedidoTipoBasicSerializer
from .pedidoEstatusSerializer import PedidoEstatusSerializer, PedidoEstatusComboSerializer, PedidoEstatusBasicSerializer
from .monedaSerializer import MonedaBasicSerializer, MonedaComboSerializer, MonedaSerializer
from .formaPagoSerializer import FormaPagoSerializer, FormaPagoBasicSerializer, FormaPagoComboSerializer
from .pedidoSerializer import PedidoSerializer, PedidoBasicSerializer, PedidoComboSerializer, PedidoHistoricoSerializer
from .pedidoDetalleSerializer import PedidoDetalleSerializer, PedidoDetalleBasicSerializer, PedidoDetalleComboSerializer
from .userSerializer import UserBasicSerializer, UserSerializer
from .bancoSerializer import BancoSerializer, BancoBasicSerializer, BancoComboSerializer
from .cuentaSerializer import CuentaBasicSerializer, CuentaComboSerializer, CuentaSerializer
from .tasaCambioSerializer import TasaCambioBasicSerializer, TasaCambioComboSerializer, TasaCambioSerializer
from .profileUserSerializer import ProfileUserBasicSerializer, ProfileUserSerializer