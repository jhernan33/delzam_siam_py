from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Auth View
    path('signup/',                     views.SignupView.as_view(), name='signup'),
    path('login/',                      views.LoginView.as_view(), name='login'),
    path('logout/',                     views.LogoutView.as_view(), name='login'),
    path('user/',                       views.UserView.as_view(), name='user'),
    path('reset/',                      views.ResetPasswordView.as_view(), name='reset_password'),

    # Grupos
    path('grupo/',                  views.GrupoListView.as_view(),     name='grupo'),
    path('grupo/create/',           views.GrupoCreateView.as_view(),   name='grupo_create'),
    path('grupo/<int:id>/',         views.GrupoRetrieveView.as_view(), name='grupo'),
    path('grupo/update/<int:id>',   views.GrupoUpdateView.as_view(),   name='grupo_update'),
    path('grupo/delete/<int:id>',   views.GrupoDestroyView.as_view(),  name='grupo_delete'),
    path('grupo/combo/',            views.GrupoComboView.as_view(),    name='grupo_combo'),

    # Grupo Usuario
    path('grupoUsuario/',                 views.GrupoListView.as_view(),     name='grupoUsuario'),
    path('grupoUsuario/create/',          views.GrupoCreateView.as_view(),   name='grupoUsuario_create'),
    path('grupoUsuario/<int:id>/',        views.GrupoRetrieveView.as_view(), name='grupoUsuario'),
    path('grupoUsuario/update/<int:id>',  views.GrupoUpdateView.as_view(),   name='grupoUsuario_update'),
    path('grupoUsuario/delete/<int:id>',  views.GrupoDestroyView.as_view(),  name='grupoUsuario_delete'),


    path('pais/',                       views.PaisListView.as_view(),     name='pais'),
    path('pais/create/',                views.PaisCreateView.as_view(),   name='pais_create'),
    path('pais/<int:id>/',              views.PaisRetrieveView.as_view(), name='pais'),
    path('pais/update/<int:id>',        views.PaisUpdateView.as_view(),   name='pais_update'),
    path('pais/delete/<int:id>',        views.PaisDestroyView.as_view(),  name='pais_delete'),
    path('pais/combo/',                 views.PaisComboView.as_view(),    name='pais_combo'),

    path('estado/',                     views.EstadoListView.as_view(),     name='estado'),
    path('estado/create/',              views.EstadoCreateView.as_view(),   name='estado_create'),
    path('estado/<int:id>/',            views.EstadoRetrieveView.as_view(), name='estado'),
    path('estado/update/<int:id>',      views.EstadoUpdateView.as_view(),   name='estado_update'),
    path('estado/delete/<int:id>',      views.EstadoDestroyView.as_view(),  name='estado_delete'),
    path('estado/combo/',               views.EstadoComboView.as_view(),    name='estado_combo'),

    path('ciudad/',                     views.CiudadListView.as_view(),     name='ciudad'),
    path('ciudad/create/',              views.CiudadCreateView.as_view(),   name='ciudad_create'),
    path('ciudad/<int:id>/',            views.CiudadRetrieveView.as_view(), name='ciudad'),
    path('ciudad/update/<int:id>',      views.CiudadUpdateView.as_view(),   name='ciudad_update'),
    path('ciudad/delete/<int:id>',      views.CiudadDestroyView.as_view(),  name='ciudad_delete'),
    path('ciudad/combo/',               views.CiudadComboView.as_view(),    name='ciudad_combo'),


    # path('municipio/',                 views.MunicipioListView.as_view(),     name='municipio'),
    # path('municipio/create/',          views.MunicipioCreateView.as_view(),   name='municipio_create'),
    # path('municipio/<int:id>/',        views.MunicipioRetrieveView.as_view(), name='municipio'),
    # path('municipio/<int:id>/update/', views.MunicipioUpdateView.as_view(),   name='municipio_update'),
    # path('municipio/<int:id>/delete/', views.MunicipioDestroyView.as_view(),  name='municipio_delete'),

    # # path('parroquias/',                views.ParroquiasListView.as_view(),     name='parroquias'),
    # # path('parroquias/create/',          views.ParroquiasCreateView.as_view(),   name='parroquias_create'),
    # # path('parroquias/<int:id>/',        views.ParroquiasRetrieveView.as_view(), name='parroquias'),
    # # path('parroquias/<int:id>/update/', views.ParroquiasUpdateView.as_view(),   name='parroquias_update'),
    # # path('parroquias/<int:id>/delete/', views.ParroquiasDestroyView.as_view(),  name='parroquias_delete'),

    path('sector/',                      views.SectorListView.as_view(),     name='sector'),
    path('sector/create/',               views.SectorCreateView.as_view(),   name='sector_create'),
    path('sector/<int:id>/',             views.SectorRetrieveView.as_view(), name='sector'),
    path('sector/update/<int:id>',       views.SectorUpdateView.as_view(),   name='sector_update'),
    path('sector/delete/<int:id>',       views.SectorDestroyView.as_view(),  name='sector_delete'),
    path('sector/combo/',                views.SectorComboView.as_view(),    name='sector_combo'),

    path('subSector/',                 views.SubSectorListView.as_view(),     name='subSector'),
    path('subSector/create/',          views.SubSectorCreateView.as_view(),   name='subSector_create'),
    path('subSector/<int:id>/',        views.SubSectorRetrieveView.as_view(), name='subSector'),
    path('subSector/update/<int:id>', views.SubSectorUpdateView.as_view(),   name='subSector_update'),
    path('subSector/delete/<int:id>', views.SubSectorDestroyView.as_view(),  name='subSector_delete'),

    path('natural/',                 views.NaturalListView.as_view(),     name='natural'),
    path('natural/create/',          views.NaturalCreateView.as_view(),   name='natural_create'),
    path('natural/<int:id>/',        views.NaturalRetrieveView.as_view(), name='natural'),
    path('natural/update/<int:id>',  views.NaturalUpdateView.as_view(),   name='natural_update'),
    path('natural/delete/<int:id>',  views.NaturalDestroyView.as_view(),  name='natural_delete'),
    path('natural/filter/',          views.NaturalFilterView.as_view(),   name='natural_filter'),
    path('natural/combo/',           views.NaturalComboView.as_view(),   name='natural_combo'),

    path('tipoempresa/',                 views.TipoEmpresaListView.as_view(),     name='tipoempresa'),
    path('tipoempresa/create/',          views.TipoEmpresaCreateView.as_view(),   name='tipoempresa_create'),
    path('tipoempresa/<int:id>/',        views.TipoEmpresaRetrieveView.as_view(), name='tipoempresa'),
    path('tipoempresa/update/<int:id>', views.TipoEmpresaUpdateView.as_view(),   name='tipoempresa_update'),
    path('tipoempresa/delete/<int:id>', views.TipoEmpresaDestroyView.as_view(),  name='tipoempresa_delete'),
    path('tipoempresa/combo/',          views.TipoEmpresaComboView.as_view(),    name='tipoempresa_combo'),

    path('juridica/',                 views.JuridicaListView.as_view(),     name='juridica'),
    path('juridica/create/',          views.JuridicaCreateView.as_view(),   name='juridica_create'),
    path('juridica/<int:id>/',        views.JuridicaRetrieveView.as_view(), name='juridica'),
    path('juridica/update/<int:id>', views.JuridicaUpdateView.as_view(),   name='juridica_update'),
    path('juridica/delete/<int:id>', views.JuridicaDestroyView.as_view(),  name='juridica_delete'),
    path('juridica/combo/',          views.JuridicaComboView.as_view(),    name='juridica_combo'),

    path('accionista/',                 views.AccionistaListView.as_view(),     name='accionista'),
    path('accionista/create/',          views.AccionistaCreateView.as_view(),   name='accionista_create'),
    path('accionista/<int:id>/',        views.AccionistaRetrieveView.as_view(), name='accionista'),
    path('accionista/update/<int:id>', views.AccionistaUpdateView.as_view(),   name='accionista_update'),
    path('accionista/delete/<int:id>', views.AccionistaDestroyView.as_view(),  name='accionista_delete'),

    path('sucursal/',                 views.SucursalListView.as_view(),     name='accionista'),
    path('sucursal/create/',          views.SucursalCreateView.as_view(),   name='accionista_create'),
    path('sucursal/<int:id>/',        views.SucursalRetrieveView.as_view(), name='accionista'),
    path('sucursal/update/<int:id>', views.SucursalUpdateView.as_view(),   name='accionista_update'),
    path('sucursal/delete/<int:id>', views.SucursalDestroyView.as_view(),  name='accionista_delete'),

    path('familia/',                 views.FamiliaListView.as_view(),     name='familia'),
    path('familia/create/',          views.FamiliaCreateView.as_view(),   name='familia_create'),
    path('familia/<int:id>/',        views.FamiliaRetrieveView.as_view(), name='familia'),
    path('familia/update/<int:id>', views.FamiliaUpdateView.as_view(),   name='familia_update'),
    path('familia/delete/<int:id>', views.FamiliaDestroyView.as_view(),  name='familia_delete'),
    path('familia/combo/',          views.FamiliaComboView.as_view(),name='familia_combo'),
    path('familia/restore/<int:id>', views.FamiliaRestore.as_view(),   name='familia_restore'),

    path('subfamilia/',                 views.SubFamiliaListView.as_view(),     name='subfamilia'),
    path('subfamilia/create/',          views.SubFamiliaCreateView.as_view(),   name='subfamilia_create'),
    path('subfamilia/<int:id>/',        views.SubFamiliaRetrieveView.as_view(), name='subfamilia'),
    path('subfamilia/update/<int:id>', views.SubFamiliaUpdateView.as_view(),   name='subfamilia_update'),
    path('subfamilia/delete/<int:id>', views.SubFamiliaDestroyView.as_view(),  name='subfamilia_delete'),
    path('subfamilia/combo/',          views.SubFamiliaComboView.as_view(),name='familia_combo'),

    path('zona/',                 views.ZonaListView.as_view(),     name='zona'),
    path('zona/create/',          views.ZonaCreateView.as_view(),   name='zona_create'),
    path('zona/<int:id>/',        views.ZonaRetrieveView.as_view(), name='zona'),
    path('zona/update/<int:id>', views.ZonaUpdateView.as_view(),    name='zona_update'),
    path('zona/delete/<int:id>', views.ZonaDestroyView.as_view(),   name='zona_delete'),
    path('zona/combo/',          views.ZonaComboView.as_view(),     name='zona_combo'),

    path('vendedor/',                 views.VendedorListView.as_view(),     name='vendedor'),
    path('vendedor/create/',          views.VendedorCreateView.as_view(),   name='vendedor_create'),
    path('vendedor/<int:id>/',        views.VendedorRetrieveView.as_view(), name='vendedor'),
    path('vendedor/update/<int:id>', views.VendedorUpdateView.as_view(),    name='vendedor_update'),
    path('vendedor/delete/<int:id>', views.VendedorDestroyView.as_view(),   name='vendedor_delete'),
    path('vendedor/combo/',          views.VendedorComboView.as_view(),     name='vendedor_combo'),

    path('ruta/',                 views.RutaListView.as_view(),     name='ruta'),
    path('ruta/create/',          views.RutaCreateView.as_view(),   name='ruta_create'),
    path('ruta/<int:id>/',        views.RutaRetrieveView.as_view(), name='ruta'),
    path('ruta/update/<int:id>',  views.RutaUpdateView.as_view(),   name='ruta_update'),
    path('ruta/delete/<int:id>',  views.RutaDestroyView.as_view(),  name='ruta_delete'),
    path('ruta/combo/',           views.RutaComboView.as_view(),    name='ruta_combo'),
    path('rutaCliente/<int:id>/', views.RutaClienteRetrieveView.as_view(), name='rutaCliente'),

    path('rutaDetalleVendedor/',                 views.RutaDetalleVendedorListView.as_view(),     name='rutaDetalleVendedor'),
    path('rutaDetalleVendedor/create/',          views.RutaDetalleVendedorCreateView.as_view(),   name='rutaDetalleVendedor_create'),
    path('rutaDetalleVendedor/<int:id>/',        views.RutaDetalleVendedorRetrieveView.as_view(), name='rutaDetalleVendedor'),
    path('rutaDetalleVendedor/update/<int:id>',  views.RutaDetalleVendedorUpdateView.as_view(),   name='rutaDetalleVendedor_update'),
    path('rutaDetalleVendedor/delete/<int:id>',  views.RutaDetalleVendedorDestroyView.as_view(),  name='rutaDetalleVendedor_delete'),
    path('rutaDetalleVendedor/combo/',           views.RutaDetalleVendedorComboView.as_view(),    name='rutaDetalleVendedor_combo'),

    # Articulo
    path('articulo/',                            views.ArticuloListView.as_view(),                name='articulo'),
    path('articulo/create/',                     views.ArticuloCreateView.as_view(),              name='articulo_create'),
    path('articulo/<int:id>/',                   views.ArticuloRetrieveView.as_view(),            name='articulo'),
    path('articulo/update/<int:id>',             views.ArticuloUpdateView.as_view(),              name='articulo_update'),
    path('articulo/delete/<int:id>',             views.ArticuloDestroyView.as_view(),             name='articulo_delete'),
    path('articulo/combo/',                      views.ArticuloComboView.as_view(),               name='articulo_combo'),
    path('articulo/buscar/',                     views.ArticuloSearch,                            name='articulo_search'),
    # Upload File DBF
    path('articulo/upload/',                     views.ArticuloComboView.as_view(),               name='articulo_upload'),

    path('unidadmedida/',                       views.UnidadMedidaListView.as_view(),     name='unidadmedida'),
    path('unidadmedida/create/',                views.UnidadMedidaCreateView.as_view(),   name='unidadmedida_create'),
    path('unidadmedida/<int:id>/',              views.UnidadMedidaRetrieveView.as_view(), name='unidadmedida'),
    path('unidadmedida/update/<int:id>',       views.UnidadMedidaUpdateView.as_view(),   name='unidadmedida_update'),
    path('unidadmedida/delete/<int:id>',       views.UnidadMedidaDestroyView.as_view(),  name='unidadmedida_delete'),

    path('unidadtributaria/',                     views.UnidadTributariaListView.as_view(),     name='unidadtributaria'),
    path('unidadtributaria/create/',              views.UnidadTributariaCreateView.as_view(),   name='unidadtributaria_create'),
    path('unidadtributaria/<int:id>/',            views.UnidadTributariaRetrieveView.as_view(), name='unidadtributaria'),
    path('unidadtributaria/update/<int:id>',     views.UnidadTributariaUpdateView.as_view(),   name='unidadtributaria_update'),
    path('unidadtributaria/delete/<int:id>',     views.UnidadTributariaDestroyView.as_view(),  name='unidadtributaria_delete'),
    
    # IVa General (Maestro)
    path('iva/',                                   views.IvaGeneralListView.as_view(),     name='iva'),
    path('iva/create/',                            views.IvaGeneralCreateView.as_view(),   name='iva_create'),
    path('iva/<int:id>/',                          views.IvaGeneralRetrieveView.as_view(), name='iva'),
    path('iva/update/<int:id>',                    views.IvaGeneralUpdateView.as_view(),   name='iva_update'),
    path('iva/delete/<int:id>',                    views.IvaGeneralDestroyView.as_view(),  name='iva_delete'),
    path('iva/combo/',                             views.IvaGeneralComboView.as_view(),    name='iva_combo'),

    # Iva Detalle
    path('ivaDetalle/',                            views.IvaListView.as_view(),     name='ivaDetalle'),
    path('ivaDetalle/create/',                     views.IvaCreateView.as_view(),   name='ivaDetalle_create'),
    path('ivaDetalle/<int:id>/',                   views.IvaRetrieveView.as_view(), name='ivaDetalle'),
    path('ivaDetalle/update/<int:id>',             views.IvaUpdateView.as_view(),   name='ivaDetalle_update'),
    path('ivaDetalle/delete/<int:id>',             views.IvaDestroyView.as_view(),  name='ivaDetalle_delete'),

    path('cliente/',                                views.ClienteListView.as_view(),     name='cliente'),
    path('cliente/create/',                         views.ClienteCreateView.as_view(),   name='cliente_create'),
    path('cliente/<int:id>/',                       views.ClienteRetrieveView.as_view(), name='cliente'),
    path('cliente/update/<int:id>',                 views.ClienteUpdateView.as_view(),   name='cliente_update'),
    path('cliente/delete/<int:id>',                 views.ClienteDestroyView.as_view(),  name='cliente_delete'),
    path('cliente/combo/',                          views.ClienteComboView.as_view(),    name='cliente_combo'),
    path('cliente/buscar/',                         views.ClienteBuscarView.as_view(),   name='cliente_find'),

    # Presentacion
    path('presentacion/',                            views.PresentacionListView.as_view(),     name='presentacion'),
    path('presentacion/create/',                     views.PresentacionCreateView.as_view(),   name='presentacion_create'),
    path('presentacion/<int:id>/',                   views.PresentacionRetrieveView.as_view(), name='presentacion'),
    path('presentacion/update/<int:id>',             views.PresentacionUpdateView.as_view(),   name='presentacion_update'),
    path('presentacion/delete/<int:id>',             views.PresentacionDestroyView.as_view(),  name='presentacion_delete'),
    path('presentacion/combo/',                      views.PresentacionComboView.as_view(),    name='presentacion_combo'),
    path('presentacion/restore/<int:id>',            views.PresentacionRestore.as_view(),      name='presentacion_restore'),

    # Supplier
    path('proveedor/',                            views.ProveedorListView.as_view(),     name='proveedor'),
    path('proveedor/create/',                     views.ProveedorCreateView.as_view(),   name='proveedor_create'),
    path('proveedor/<int:id>/',                   views.ProveedorRetrieveView.as_view(), name='proveedor'),
    path('proveedor/update/<int:id>',             views.ProveedorUpdateView.as_view(),   name='proveedor_update'),
    path('proveedor/delete/<int:id>',             views.ProveedorDestroyView.as_view(),  name='proveedor_delete'),
    path('proveedor/combo/',                      views.ProveedorComboView.as_view(),    name='proveedor_combo'),
    path('proveedor/restore/<int:id>',            views.ProveedorRestore.as_view(),      name='proveedor_restore'),

    # Article Supplier
    path('proveedorArticulo/',                    views.ArticuloProveedorListView.as_view(),     name='proveedorArticulo'),
    path('proveedorArticulo/create/',             views.ArticuloProveedorCreateView.as_view(),   name='proveedorArticulo_create'),
    path('proveedorArticulo/<int:id>/',           views.ArticuloProveedorRetrieveView.as_view(), name='proveedorArticulo'),
    path('proveedorArticulo/update/<int:id>',     views.ArticuloProveedorUpdateView.as_view(),   name='proveedorArticulo_update'),
    path('proveedorArticulo/delete/<int:id>',     views.ArticuloProveedorDestroyView.as_view(),  name='proveedorArticulo_delete'),
    path('proveedorArticulo/combo/',              views.ArticuloProveedorComboView.as_view(),    name='proveedorArticulo_combo'),

    # Category Contact
    path('categoriaContacto/',                    views.CategoriaContactoListView.as_view(),     name='categoriaContacto'),
    path('categoriaContacto/create/',             views.CategoriaContactoCreateView.as_view(),   name='categoriaContacto_create'),
    path('categoriaContacto/<int:id>/',           views.CategoriaContactoRetrieveView.as_view(), name='categoriaContacto'),
    path('categoriaContacto/update/<int:id>',     views.CategoriaContactoUpdateView.as_view(),   name='categoriaContacto_update'),
    path('categoriaContacto/delete/<int:id>',     views.CategoriaContactoDestroyView.as_view(),  name='categoriaContacto_delete'),
    path('categoriaContacto/combo/',              views.CategoriaContactoComboView.as_view(),    name='categoriaContacto_combo'),

    # Group Category Contact
    path('grupocc/',                              views.GrupoCategoriaContactoListView.as_view(),     name='grupoCategoriaContacto'),
    path('grupocc/create/',                       views.GrupoCategoriaContactoCreateView.as_view(),   name='grupoCategoriaContacto_create'),
    path('grupocc/<int:id>/',                     views.GrupoCategoriaContactoRetrieveView.as_view(), name='grupoCategoriaContacto'),
    path('grupocc/update/<int:id>',               views.GrupoCategoriaContactoUpdateView.as_view(),   name='grupoCategoriaContacto_update'),
    path('grupocc/delete/<int:id>',               views.GrupoCategoriaContactoDestroyView.as_view(),  name='grupoCategoriaContacto_delete'),
    path('grupocc/combo/',                        views.GrupoCategoriaContactoComboView.as_view(),    name='grupoCategoriaContacto_combo'),

    # Search Filter by Field
    path('configuracion/busquedad/',             views.ConfiguracionBusquedadListView.as_view(),                name='List Fields Busquedad'),

    # Type of Order
    path('pedidotipo/',                              views.PedidoTipoListView.as_view(),     name='pedidotipo'),
    path('pedidotipo/create/',                       views.PedidoTipoCreateView.as_view(),   name='pedidotipo_create'),
    path('pedidotipo/<int:id>/',                     views.PedidoTipoRetrieveView.as_view(), name='pedidotipo_show'),
    path('pedidotipo/update/<int:id>',               views.PedidoTipoUpdateView.as_view(),   name='pedidotipo_update'),
    path('pedidotipo/delete/<int:id>',               views.PedidoTipoDestroyView.as_view(),  name='pedidotipo_delete'),
    path('pedidotipo/combo/',                        views.PedidoTipoComboView.as_view(),    name='pedidotipo_combo'),

    # Type of State Order
    path('pedidoestatus/',                              views.PedidoEstatusListView.as_view(),     name='pedidoestatus'),
    path('pedidoestatus/create/',                       views.PedidoEstatusCreateView.as_view(),   name='pedidoestatus_create'),
    path('pedidoestatus/<int:id>/',                     views.PedidoEstatusRetrieveView.as_view(), name='pedidoestatus_show'),
    path('pedidoestatus/update/<int:id>',               views.PedidoEstatusUpdateView.as_view(),   name='pedidoestatus_update'),
    path('pedidoestatus/delete/<int:id>',               views.PedidoEstatusDestroyView.as_view(),  name='pedidoestatus_delete'),
    path('pedidoestatus/combo/',                        views.PedidoEstatusComboView.as_view(),    name='pedidoestatus_combo'),

    # Currency
    path('moneda/',                                     views.MonedaListView.as_view(),     name='moneda'),
    path('moneda/create/',                              views.MonedaCreateView.as_view(),   name='moneda_create'),
    path('moneda/<int:id>/',                            views.MonedaRetrieveView.as_view(), name='moneda_show'),
    path('moneda/update/<int:id>',                     views.MonedaUpdateView.as_view(),   name='moneda_update'),
    path('moneda/delete/<int:id>',                     views.MonedaDestroyView.as_view(),  name='moneda_delete'),
    path('moneda/combo/',                               views.MonedaComboView.as_view(),    name='moneda_combo'),

    # Currency Denomination
    path('denominacion/',                               views.MonedaDenominacionListView.as_view(),     name='denominacion'),
    path('denominacion/create/',                        views.MonedaDenominacionCreateView.as_view(),   name='denominacion_create'),
    path('denominacion/<int:id>/',                      views.MonedaDenominacionRetrieveView.as_view(), name='denominacion_show'),
    path('denominacion/update/<int:id>',                views.MonedaDenominacionUpdateView.as_view(),   name='denominacion_update'),
    path('denominacion/delete/<int:id>',                views.MonedaDenominacionDestroyView.as_view(),  name='denominacion_delete'),
    path('denominacion/combo/',                         views.MonedaDenominacionComboView.as_view(),    name='denominacion_combo'),

    # Way to Pay
    path('formapago/',                                      views.FormaPagoListView.as_view(),     name='formadepago'),
    path('formapago/create/',                               views.FormaPagoCreateView.as_view(),   name='formadepago_create'),
    path('formapago/<int:id>/',                             views.FormaPagoRetrieveView.as_view(), name='formadepago_show'),
    path('formapago/update/<int:id>',                       views.FormaPagoUpdateView.as_view(),   name='formadepago_update'),
    path('formapago/delete/<int:id>',                       views.FormaPagoDestroyView.as_view(),  name='formadepago_delete'),
    path('formapago/combo/',                                views.FormaPagoComboView.as_view(),    name='formadepago_combo'),

    # Orders
    path('pedido/',                                      views.PedidoListView.as_view(),     name='pedido'),
    path('pedido/create/',                               views.PedidoCreateView.as_view(),   name='pedido_create'),
    path('pedido/<int:id>/',                             views.PedidoRetrieveView.as_view(), name='pedido_show'),
    path('pedido/update/<int:id>',                       views.PedidoUpdateView.as_view(),   name='pedido_update'),
    path('pedido/delete/<int:id>',                       views.PedidoDestroyView.as_view(),  name='pedido_delete'),
    path('pedido/combo/',                                views.PedidoComboView.as_view(),    name='pedido_combo'),
    # Historical Orders
    path('pedido/historico/',                            views.PedidoHistorico.as_view(),   name='pedido_historico'),
    path('pedido/historico/update/<int:id>',             views.PedidoHistoricoUpdateView.as_view(),   name='pedido_historico_update'),
    path('pedido/state/update/<int:id>',                 views.PedidoUpdateStatusView.as_view(),   name='pedido_update_status'),
    path('pedido/historico/search/',                     views.PedidoSearchView.as_view(),   name='pedido_search'),
    # search invoice number
    path('order/search/invoice/',                       views.HistoricalOrderSearchView.as_view(),   name='pedido_search_invoice'),

    # Order Message
    path('pedidomensaje/',                              views.PedidoMensajeListView.as_view(),     name='pedidoMensaje'),
    path('pedidomensaje/create/',                       views.PedidoMensajeCreateView.as_view(),   name='pedidoMensaje_create'),
    path('pedidomensaje/<int:id>/',                     views.PedidoMensajeRetrieveView.as_view(), name='pedidoMensaje_show'),
    path('pedidomensaje/update/<int:id>',               views.PedidoMensajeUpdateView.as_view(),   name='pedidoMensaje_update'),
    path('pedidomensaje/delete/<int:id>',               views.PedidoMensajeDestroyView.as_view(),  name='pedidoMensaje_delete'),
    path('pedidomensaje/combo/',                        views.PedidoMensajeComboView.as_view(),    name='pedidoMensaje_combo'),

    # Pay 
    path('pago/',                                       views.PedidoPagoListView.as_view(),     name='pay'),
    path('pago/create/',                                views.PedidoPagoCreateView.as_view(),   name='pay_create'),
    path('pago/<int:id>/',                              views.PedidoPagoRetrieveView.as_view(), name='pay_show'),
    path('pago/update/<int:id>',                        views.PedidoPagoUpdateView.as_view(),   name='pay_update'),
    path('pago/delete/<int:id>',                        views.PedidoPagoDestroyView.as_view(),  name='pay_delete'),
    path('pago/combo/',                                 views.PedidoPagoComboView.as_view(),    name='pay_combo'), 


    # Bank
    path('banco/',                                       views.BancoListView.as_view(),     name='banco'),
    path('banco/create/',                                views.BancoCreateView.as_view(),   name='banco_create'),
    path('banco/<int:id>/',                              views.BancoRetrieveView.as_view(), name='banco'),
    path('banco/update/<int:id>',                        views.BancoUpdateView.as_view(),   name='banco_update'),
    path('banco/delete/<int:id>',                        views.BancoDestroyView.as_view(),  name='banco_delete'),
    path('banco/combo/',                                 views.BancoComboView.as_view(),   name='banco_combo'),

    # Bank Account Number
    path('cuenta/',                                       views.CuentaListView.as_view(),     name='cuenta'),
    path('cuenta/create/',                                views.CuentaCreateView.as_view(),   name='cuenta_create'),
    path('cuenta/<int:id>/',                              views.CuentaRetrieveView.as_view(), name='cuenta'),
    path('cuenta/update/<int:id>',                        views.CuentaUpdateView.as_view(),   name='cuenta_update'),
    path('cuenta/delete/<int:id>',                        views.CuentaDestroyView.as_view(),  name='cuenta_delete'),
    path('cuenta/combo/',                                 views.CuentaComboView.as_view(),    name='cuenta_combo'),

    # Exchange Rate
    path('tasa/',                                         views.TasaCambioListView.as_view(),     name='exchange_rate'),
    path('tasa/create/',                                  views.TasaCambioCreateView.as_view(),   name='exchange_rate_create'),
    path('tasa/<int:id>/',                                views.TasaCambioRetrieveView.as_view(), name='exchange_rate'),
    path('tasa/update/<int:id>',                          views.TasaCambioUpdateView.as_view(),   name='exchange_rate_update'),
    path('tasa/delete/<int:id>',                          views.TasaCambioDestroyView.as_view(),  name='exchange_rate_delete'),
    path('tasa/combo/',                                   views.TasaCambioComboView.as_view(),    name='exchange_rate_combo'),

    # Profile
    path('perfil/',                                       views.ProfileUserListView.as_view(),     name='profile'),
    path('perfil/create/',                                views.ProfileUserCreateView.as_view(),   name='profile_create'),
    path('perfil/<int:id>/',                              views.ProfileUserRetrieveView.as_view(), name='profile'),
    path('perfil/update/<int:id>',                        views.ProfileUserUpdateView.as_view(),   name='profile_update'),
    path('perfil/delete/<int:id>',                        views.ProfileUserDestroyView.as_view(),  name='profile_delete'),

    # Collector
    path('cobrador/',                                     views.CobradorListView.as_view(),     name='collector'),
    path('cobrador/create/',                              views.CobradorCreateView.as_view(),   name='collector_create'),
    path('cobrador/<int:id>/',                            views.CobradorRetrieveView.as_view(), name='collector'),
    path('cobrador/update/<int:id>',                      views.CobradorUpdateView.as_view(),   name='collector_update'),
    path('cobrador/delete/<int:id>',                      views.CobradorDestroyView.as_view(),  name='collector_delete'),
    path('cobrador/combo/',                               views.CobradorComboView.as_view(),    name='collector_combo'),

    # Date
    path('date/', views.DateRetrieveView.as_view(), name='date_get'),

    # Upload File Dbf
    path('upload/', views.FileUploadAPIView.as_view(), name='upload_article'),
    # Upload File CSV
    path('importSiae/',views.FileUploadSiaeView.as_view(), name='upload_siae_article'),
    # Upload File CSV Family
    path('importFamily/',views.FileUploadFamily.as_view(), name='upload_family'),
    # Upload File CSV SubFamily
    path('importSubFamily/',views.FileUploadSubFamily.as_view(), name='upload_sub_family'),

    # Reports
    path('report/client/route/',                views.ClienteReportView.as_view(),      name='Report Client for Route'),
    path('report/export/',                      views.export_pdf,                       name="export-pdf"), 
    path('report/history/customer/',            views.HistoryCustomer.as_view(),      name='report_history_customer'),
    path('report/export/customer/',             views.ClienteExportFile,          name='Report Pdf Customer'),
    path('report/export/histoyCustomer/',       views.exportHistoryCustomer,      name='report export history customer'),
    # Report Order
    path('report/order/',                       views.PedidoReport,      name='Report_order'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

