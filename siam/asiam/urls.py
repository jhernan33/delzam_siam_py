from django.urls import path
from . import views

urlpatterns = [

    path('pais/',                 views.PaisListView.as_view(),     name='pais'),
    path('pais/create/',          views.PaisCreateView.as_view(),   name='pais_create'),
    path('pais/<int:id>/',        views.PaisRetrieveView.as_view(), name='pais'),
    path('pais/update/<int:id>', views.PaisUpdateView.as_view(),   name='pais_update'),
    path('pais/<int:id>/delete/', views.PaisDestroyView.as_view(),  name='pais_delete'),
    path('pais/combo/<int:id>',   views.PaisComboView.as_view(),    name='pais_combo'),

    path('estado/',                     views.EstadoListView.as_view(),     name='estado'),
    path('estado/create/',              views.EstadoCreateView.as_view(),   name='estado_create'),
    path('estado/<int:id>/',            views.EstadoRetrieveView.as_view(), name='estado'),
    path('estado/update/<int:id>',     views.EstadoUpdateView.as_view(),   name='estado_update'),
    path('estado/delete/<int:id>',      views.EstadoDestroyView.as_view(),  name='estado_delete'),
    path('estado/combo/<int:id>',       views.EstadoComboView.as_view(),    name='estado_combo'),

    path('ciudad/',                     views.CiudadListView.as_view(),     name='ciudad'),
    path('ciudad/create/',              views.CiudadCreateView.as_view(),   name='ciudad_create'),
    path('ciudad/<int:id>/',            views.CiudadRetrieveView.as_view(), name='ciudad'),
    path('ciudad/update/<int:id>',     views.CiudadUpdateView.as_view(),   name='ciudad_update'),
    path('ciudad/delete/<int:id>',      views.CiudadDestroyView.as_view(),  name='ciudad_delete'),
    path('ciudad/combo/<int:id>',       views.CiudadComboView.as_view(),    name='ciudad_combo'),


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

    path('sector/',                 views.SectorListView.as_view(),     name='sector'),
    path('sector/create/',          views.SectorCreateView.as_view(),   name='sector_create'),
    path('sector/<int:id>/',        views.SectorRetrieveView.as_view(), name='sector'),
    path('sector/update/<int:id>', views.SectorUpdateView.as_view(),   name='sector_update'),
    path('sector/delete/<int:id>', views.SectorDestroyView.as_view(),  name='sector_delete'),

    path('subSector/',                 views.SubSectorListView.as_view(),     name='subSector'),
    path('subSector/create/',          views.SubSectorCreateView.as_view(),   name='subSector_create'),
    path('subSector/<int:id>/',        views.SubSectorRetrieveView.as_view(), name='subSector'),
    path('subSector/update/<int:id>', views.SubSectorUpdateView.as_view(),   name='subSector_update'),
    path('subSector/delete/<int:id>', views.SubSectorDestroyView.as_view(),  name='subSector_delete'),

    path('natural/',                 views.NaturalListView.as_view(),     name='natural'),
    path('natural/create/',          views.NaturalCreateView.as_view(),   name='natural_create'),
    path('natural/<int:id>/',        views.NaturalRetrieveView.as_view(), name='natural'),
    path('natural/update/<int:id>', views.NaturalUpdateView.as_view(),   name='natural_update'),
    path('natural/delete/<int:id>', views.NaturalDestroyView.as_view(),  name='natural_delete'),
    path('natural/filter/',          views.NaturalFilterView.as_view(),   name='natural_filter'),

    path('tipoempresa/',                 views.TipoEmpresaListView.as_view(),     name='tipoempresa'),
    path('tipoempresa/create/',          views.TipoEmpresaCreateView.as_view(),   name='tipoempresa_create'),
    path('tipoempresa/<int:id>/',        views.TipoEmpresaRetrieveView.as_view(), name='tipoempresa'),
    path('tipoempresa/update/<int:id>', views.TipoEmpresaUpdateView.as_view(),   name='tipoempresa_update'),
    path('tipoempresa/delete/<int:id>', views.TipoEmpresaDestroyView.as_view(),  name='tipoempresa_delete'),

    path('juridica/',                 views.JuridicaListView.as_view(),     name='juridica'),
    path('juridica/create/',          views.JuridicaCreateView.as_view(),   name='juridica_create'),
    path('juridica/<int:id>/',        views.JuridicaRetrieveView.as_view(), name='juridica'),
    path('juridica/update/<int:id>', views.JuridicaUpdateView.as_view(),   name='juridica_update'),
    path('juridica/delete/<int:id>', views.JuridicaDestroyView.as_view(),  name='juridica_delete'),

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

    path('subfamilia/',                 views.SubFamiliaListView.as_view(),     name='subfamilia'),
    path('subfamilia/create/',          views.SubFamiliaCreateView.as_view(),   name='subfamilia_create'),
    path('subfamilia/<int:id>/',        views.SubFamiliaRetrieveView.as_view(), name='subfamilia'),
    path('subfamilia/update/<int:id>', views.SubFamiliaUpdateView.as_view(),   name='subfamilia_update'),
    path('subfamilia/delete/<int:id>', views.SubFamiliaDestroyView.as_view(),  name='subfamilia_delete'),

    path('zona/',                 views.ZonaListView.as_view(),     name='zona'),
    path('zona/create/',          views.ZonaCreateView.as_view(),   name='zona_create'),
    path('zona/<int:id>/',        views.ZonaRetrieveView.as_view(), name='zona'),
    path('zona/update/<int:id>', views.ZonaUpdateView.as_view(),   name='zona_update'),
    path('zona/delete/<int:id>', views.ZonaDestroyView.as_view(),  name='zona_delete'),

    path('vendedor/',                 views.VendedorListView.as_view(),     name='vendedor'),
    path('vendedor/create/',          views.VendedorCreateView.as_view(),   name='vendedor_create'),
    path('vendedor/<int:id>/',        views.VendedorRetrieveView.as_view(), name='vendedor'),
    path('vendedor/update/<int:id>', views.VendedorUpdateView.as_view(),   name='vendedor_update'),
    path('vendedor/delete/<int:id>', views.VendedorDestroyView.as_view(),  name='vendedor_delete'),

    path('ruta/',                 views.RutaListView.as_view(),     name='ruta'),
    path('ruta/create/',          views.RutaCreateView.as_view(),   name='ruta_create'),
    path('ruta/<int:id>/',        views.RutaRetrieveView.as_view(), name='ruta'),
    path('ruta/update/<int:id>', views.RutaUpdateView.as_view(),   name='ruta_update'),
    path('ruta/delete/<int:id>', views.RutaDestroyView.as_view(),  name='ruta_delete'),

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

    path('iva/',                             views.IvaListView.as_view(),     name='iva'),
    path('iva/create/',                      views.IvaCreateView.as_view(),   name='iva_create'),
    path('iva/<int:id>/',                    views.IvaRetrieveView.as_view(), name='iva'),
    path('iva/update/<int:id>',             views.IvaUpdateView.as_view(),   name='iva_update'),
    path('iva/delete/<int:id>',             views.IvaDestroyView.as_view(),  name='iva_delete'),



    # path('banco/',                 views.BancoListView.as_view(),     name='banco'),
    # path('banco/create/',          views.BancoCreateView.as_view(),   name='banco_create'),
    # path('banco/<int:id>/',        views.BancoRetrieveView.as_view(), name='banco'),
    # path('banco/<int:id>/update/', views.BancoUpdateView.as_view(),   name='banco_update'),
    # path('banco/<int:id>/delete/', views.BancoDestroyView.as_view(),  name='banco_delete'),

    # path('cuenta/',                 views.CuentaListView.as_view(),     name='cuenta'),
    # path('cuenta/create/',          views.CuentaCreateView.as_view(),   name='cuenta_create'),
    # path('cuenta/<int:id>/',        views.CuentaRetrieveView.as_view(), name='cuenta'),
    # path('cuenta/<int:id>/update/', views.CuentaUpdateView.as_view(),   name='cuenta_update'),
    # path('cuenta/<int:id>/delete/', views.CuentaDestroyView.as_view(),  name='cuenta_delete'),

    # path('agencia/',                 views.AgenciaListView.as_view(),     name='agencia'),
    # path('agencia/create/',          views.AgenciaCreateView.as_view(),   name='agencia_create'),
    # path('agencia/<int:id>/',        views.AgenciaRetrieveView.as_view(), name='agencia'),
    # path('agencia/<int:id>/update/', views.AgenciaUpdateView.as_view(),   name='agencia_update'),
    # path('agencia/<int:id>/delete/', views.AgenciaDestroyView.as_view(),  name='agencia_delete'),

    # path('articulo/',                        views.ArticuloListView.as_view(),     name='articulo'),
    # path('articulo/create/',                 views.ArticuloCreateView.as_view(),   name='articulo_create'),
    # path('articulo/<int:id>/',               views.ArticuloRetrieveView.as_view(), name='articulo'),
    # path('articulo/<int:id>/update/',        views.ArticuloUpdateView.as_view(),   name='articulo_update'),
    # path('articulo/<int:id>/delete/',        views.ArticuloDestroyView.as_view(),  name='articulo_delete'),

    # path('cmarco/',                          views.CmarcoListView.as_view(),     name='cmarco'),
    # path('cmarco/create/',                   views.CmarcoCreateView.as_view(),   name='cmarco_create'),
    # path('cmarco/<int:id>/',                 views.CmarcoRetrieveView.as_view(), name='cmarco'),
    # path('cmarco/<int:id>/update/',          views.CmarcoUpdateView.as_view(),   name='cmarco_update'),
    # path('cmarco/<int:id>/delete/',          views.CmarcoDestroyView.as_view(),  name='cmarco_delete'),

    # path('cpago/',                           views.CpagoListView.as_view(),     name='cpago'),
    # path('cpago/create/',                    views.CpagoCreateView.as_view(),   name='cpago_create'),
    # path('cpago/<int:id>/',                  views.CpagoRetrieveView.as_view(), name='cpago'),
    # path('cpago/<int:id>/update/',           views.CpagoUpdateView.as_view(),   name='cpago_update'),
    # path('cpago/<int:id>/delete/',           views.CpagoDestroyView.as_view(),  name='cpago_delete'),

    # path('fpago/',                           views.FpagoListView.as_view(),     name='fpago'),
    # path('fpago/create/',                    views.FpagoCreateView.as_view(),   name='fpago_create'),
    # path('fpago/<int:id>/',                  views.FpagoRetrieveView.as_view(), name='fpago'),
    # path('fpago/<int:id>/update/',           views.FpagoUpdateView.as_view(),   name='fpago_update'),
    # path('fpago/<int:id>/delete/',           views.FpagoDestroyView.as_view(),  name='fpago_delete'),

    # path('ginstruccion/',                    views.GinstruccionListView.as_view(),     name='ginstruccion'),
    # path('ginstruccion/create/',             views.GinstruccionCreateView.as_view(),   name='ginstruccion_create'),
    # path('ginstruccion/<int:id>/',           views.GinstruccionRetrieveView.as_view(), name='ginstruccion'),
    # path('ginstruccion/<int:id>/update/',    views.GinstruccionUpdateView.as_view(),   name='ginstruccion_update'),
    # path('ginstruccion/<int:id>/delete/',    views.GinstruccionDestroyView.as_view(),  name='ginstruccion_delete'),

    # path('monedas/',                         views.MonedasListView.as_view(),     name='monedas'),
    # path('monedas/create/',                  views.MonedasCreateView.as_view(),   name='monedas_create'),
    # path('monedas/<int:id>/',                views.MonedasRetrieveView.as_view(), name='monedas'),
    # path('monedas/<int:id>/update/',         views.MonedasUpdateView.as_view(),   name='monedas_update'),
    # path('monedas/<int:id>/delete/',         views.MonedasDestroyView.as_view(),  name='monedas_delete'),

    # path('pcontratacion/',                   views.PcontratacionListView.as_view(),     name='pcontratacion'),
    # path('pcontratacion/create/',            views.PcontratacionCreateView.as_view(),   name='pcontratacion_create'),
    # path('pcontratacion/<int:id>/',          views.PcontratacionRetrieveView.as_view(), name='pcontratacion'),
    # path('pcontratacion/<int:id>/update/',   views.PcontratacionUpdateView.as_view(),   name='pcontratacion_update'),
    # path('pcontratacion/<int:id>/delete/',   views.PcontratacionDestroyView.as_view(),  name='pcontratacion_delete'),

    # path('presupuesto/',                     views.PresupuestoListView.as_view(),     name='presupuesto'),
    # path('presupuesto/create/',              views.PresupuestoCreateView.as_view(),   name='presupuesto_create'),
    # path('presupuesto/<int:id>/',            views.PresupuestoRetrieveView.as_view(), name='presupuesto'),
    # path('presupuesto/<int:id>/update/',     views.PresupuestoUpdateView.as_view(),   name='presupuesto_update'),
    # path('presupuesto/<int:id>/delete/',     views.PresupuestoDestroyView.as_view(),  name='presupuesto_delete'),

    # path('profesiones/',                     views.ProfesionesListView.as_view(),     name='profesiones'),
    # path('profesiones/create/',              views.ProfesionesCreateView.as_view(),   name='profesiones_create'),
    # path('profesiones/<int:id>/',            views.ProfesionesRetrieveView.as_view(), name='profesiones'),
    # path('profesiones/<int:id>/update/',     views.ProfesionesUpdateView.as_view(),   name='profesiones_update'),
    # path('profesiones/<int:id>/delete/',     views.ProfesionesDestroyView.as_view(),  name='profesiones_delete'),

    # path('tclientes/',                       views.TclientesListView.as_view(),     name='tclientes'),
    # path('tclientes/create/',                views.TclientesCreateView.as_view(),   name='tclientes_create'),
    # path('tclientes/<int:id>/',              views.TclientesRetrieveView.as_view(), name='tclientes'),
    # path('tclientes/<int:id>/update/',       views.TclientesUpdateView.as_view(),   name='tclientes_update'),
    # path('tclientes/<int:id>/delete/',       views.TclientesDestroyView.as_view(),  name='tclientes_delete'),

    # path('waletr/',                          views.WaletrListView.as_view(),     name='waletr'),
    # path('waletr/create/',                   views.WaletrCreateView.as_view(),   name='waletr_create'),
    # path('waletr/<int:id>/',                 views.WaletrRetrieveView.as_view(), name='waletr'),
    # path('waletr/<int:id>/update/',          views.WaletrUpdateView.as_view(),   name='waletr_update'),
    # path('waletr/<int:id>/delete/',          views.WaletrDestroyView.as_view(),  name='waletr_delete'),

]
