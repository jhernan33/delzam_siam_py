from .paisView     import PaisListView,     PaisCreateView,     PaisRetrieveView,     PaisUpdateView,     PaisDestroyView      ,PaisComboView
from .estadoView   import EstadoListView,    EstadoCreateView,    EstadoRetrieveView,    EstadoUpdateView,    EstadoDestroyView     ,EstadoComboView
from .ciudadView   import CiudadListView,    CiudadCreateView,    CiudadRetrieveView,    CiudadUpdateView,    CiudadDestroyView     ,CiudadComboView
# from .municipioView import MunicipioListView, MunicipioCreateView, MunicipioRetrieveView, MunicipioUpdateView, MunicipioDestroyView
# from .parroquiaView import ParroquiaListView, ParroquiaCreateView, ParroquiaRetrieveView, ParroquiaUpdateView, ParroquiaDestroyView
from .sectorView  import SectorListView,   SectorCreateView,   SectorRetrieveView,   SectorUpdateView,   SectorDestroyView, SectorComboView
from .subSectorView import SubSectorListView, SubSectorCreateView, SubSectorRetrieveView, SubSectorUpdateView, SubSectorDestroyView
from .naturalView import NaturalListView, NaturalCreateView, NaturalRetrieveView, NaturalUpdateView, NaturalDestroyView, NaturalFilterView, NaturalComboView
from .tipoEmpresaView import TipoEmpresaListView, TipoEmpresaCreateView, TipoEmpresaRetrieveView, TipoEmpresaUpdateView, TipoEmpresaDestroyView,TipoEmpresaComboView
from .juridicaView import JuridicaListView, JuridicaCreateView, JuridicaRetrieveView, JuridicaUpdateView, JuridicaDestroyView, JuridicaComboView
from .acccionistaView import AccionistaListView, AccionistaCreateView, AccionistaRetrieveView, AccionistaUpdateView, AccionistaDestroyView
from .sucursalView import SucursalListView, SucursalCreateView, SucursalRetrieveView, SucursalUpdateView, SucursalDestroyView
from .tipoClienteView import TipoClienteListView, TipoClienteCreateView, TipoClienteRetrieveView, TipoClienteUpdateView, TipoClienteDestroyView
from .familiaView import FamiliaListView, FamiliaCreateView, FamiliaRetrieveView, FamiliaUpdateView, FamiliaDestroyView,FamiliaComboView, FamiliaRestore
from .subFamiliaView import SubFamiliaListView, SubFamiliaCreateView, SubFamiliaRetrieveView, SubFamiliaUpdateView, SubFamiliaDestroyView, SubFamiliaComboView
from .zonaView import ZonaListView, ZonaCreateView, ZonaRetrieveView, ZonaUpdateView, ZonaDestroyView,ZonaComboView
from .vendedorView import VendedorListView, VendedorCreateView, VendedorRetrieveView, VendedorUpdateView, VendedorDestroyView, VendedorComboView
from .rutaView import RutaListView, RutaCreateView, RutaRetrieveView, RutaUpdateView, RutaDestroyView, RutaComboView
from .unidadMedidaView  import UnidadMedidaListView, UnidadMedidaCreateView, UnidadMedidaRetrieveView, UnidadMedidaUpdateView, UnidadMedidaDestroyView
from .ivaView           import IvaListView, IvaCreateView, IvaRetrieveView, IvaUpdateView, IvaDestroyView
from .unidadTributariaView import UnidadTributariaListView, UnidadTributariaCreateView, UnidadTributariaRetrieveView, UnidadTributariaUpdateView, UnidadTributariaDestroyView
from .clienteView       import ClienteListView, ClienteCreateView, ClienteRetrieveView, ClienteUpdateView, ClienteDestroyView
from .userView          import SignupView, LoginView, LogoutView
from .grupoView         import GrupoListView, GrupoCreateView, GrupoDestroyView, GrupoRetrieveView, GrupoUpdateView
from .rutaDetalleVendedorView import RutaDetalleVendedorListView, RutaDetalleVendedorCreateView, RutaDetalleVendedorRetrieveView, RutaDetalleVendedorDestroyView, RutaDetalleVendedorUpdateView ,RutaDetalleVendedorComboView
from .ivaGeneralView    import IvaGeneralListView, IvaGeneralCreateView, IvaGeneralRetrieveView, IvaGeneralUpdateView, IvaGeneralDestroyView, IvaGeneralComboView
from .articuloView     import ArticuloListView, ArticuloCreateView, ArticuloRetrieveView, ArticuloUpdateView, ArticuloDestroyView, ArticuloComboView
from .presentacionView import PresentacionListView, PresentacionCreateView, PresentacionRetrieveView, PresentacionUpdateView, PresentacionDestroyView, PresentacionComboView, PresentacionRestore
from .serviceImageView import ServiceImageView
from .proveedorView    import ProveedorListView, ProveedorCreateView, ProveedorRetrieveView, ProveedorUpdateView, ProveedorDestroyView, ProveedorComboView, ProveedorRestore
from .articuloProveedorView import ArticuloProveedorListView, ArticuloProveedorCreateView, ArticuloProveedorRetrieveView, ArticuloProveedorUpdateView, ArticuloProveedorDestroyView, ArticuloProveedorComboView

# from .grupoUsuarioView  import GrupoUsuarioListView, GrupoUsuarioCreateView, GrupoUsuarioDestroyView, GrupoUsuarioRetrieveView, GrupoUsuarioUpdateView
# from .baseMensajeView import BaseMessage

# from .banco import BancoListView, BancoCreateView, BancoRetrieveView, BancoUpdateView, BancoDestroyView
# from .cuenta import CuentaListView, CuentaCreateView, CuentaRetrieveView, CuentaUpdateView, CuentaDestroyView
# from .agencia import AgenciaListView, AgenciaCreateView, AgenciaRetrieveView, AgenciaUpdateView, AgenciaDestroyView

# from .cmarco          import CmarcoListView, CmarcoCreateView, CmarcoRetrieveView, CmarcoUpdateView, CmarcoDestroyView
# from .cpago           import CpagoListView, CpagoCreateView, CpagoRetrieveView, CpagoUpdateView, CpagoDestroyView
# from .fpago           import FpagoListView, FpagoCreateView, FpagoRetrieveView, FpagoUpdateView, FpagoDestroyView
# from .ginstruccion    import GinstruccionListView, GinstruccionCreateView, GinstruccionRetrieveView, GinstruccionUpdateView, GinstruccionDestroyView

# from .monedas         import MonedasListView, MonedasCreateView, MonedasRetrieveView, MonedasUpdateView, MonedasDestroyView
# from .pcontratacion   import PcontratacionListView, PcontratacionCreateView, PcontratacionRetrieveView, PcontratacionUpdateView, PcontratacionDestroyView
# from .presupuesto     import PresupuestoListView, PresupuestoCreateView, PresupuestoRetrieveView, PresupuestoUpdateView, PresupuestoDestroyView
# from .profesiones     import ProfesionesListView, ProfesionesCreateView, ProfesionesRetrieveView, ProfesionesUpdateView, ProfesionesDestroyView
# from .tclientes       import TclientesListView, TclientesCreateView, TclientesRetrieveView, TclientesUpdateView, TclientesDestroyView
# from .tcomunicaciones import TcomunicacionesListView, TcomunicacionesCreateView, TcomunicacionesRetrieveView, TcomunicacionesUpdateView, TcomunicacionesDestroyView

# from .waletr          import WaletrListView, WaletrCreateView, WaletrRetrieveView, WaletrUpdateView, WaletrDestroyView
